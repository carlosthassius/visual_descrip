import numpy as np
from PIL import Image

class EHDDescriptor:
    QuantTable = np.array([
        [0.010867, 0.057915, 0.099526, 0.144849, 0.195573, 0.260504, 0.358031, 0.530128],
        [0.012266, 0.069934, 0.125879, 0.182307, 0.243396, 0.314563, 0.411728, 0.564319],
        [0.004193, 0.025852, 0.046860, 0.068519, 0.093286, 0.123490, 0.161505, 0.228960],
        [0.004174, 0.025924, 0.046232, 0.067163, 0.089655, 0.115391, 0.151904, 0.217745],
        [0.006778, 0.051667, 0.108650, 0.166257, 0.224226, 0.285691, 0.356375, 0.450972]
    ])

    def __init__(self, threshold=50):
        self.threshold = threshold
        self.BIN_COUNT = 80
        self.Local_Edge_Histogram = np.zeros(80)
        self.num_block = 1100

        self.NoEdge = 0
        self.vertical_edge = 1
        self.horizontal_edge = 2
        self.non_directional_edge = 3
        self.diagonal_45_degree_edge = 4
        self.diagonal_135_degree_edge = 5

    def apply(self, image: Image.Image):
        image = image.convert('RGB')
        self.width, self.height = image.size
        self.blockSize = self._get_block_size()

        # Converter para escala de cinza com luminância Y
        pixels = np.array(image).astype(np.float32)
        Y = (0.114 * pixels[:, :, 2] + 0.587 * pixels[:, :, 1] + 0.299 * pixels[:, :, 0]) / 256.0
        self.grey_level = (219.0 * Y + 16.5).astype(np.float32)

        return self.extract_feature()

    def _get_block_size(self):
        a = np.sqrt((self.width * self.height) / self.num_block)
        bsize = int(np.floor(a / 2) * 2)
        return max(bsize, 2)

    def _get_block_avg(self, x, y, dx, dy):
        block = self.grey_level[x + dx:x + dx + self.blockSize // 2,
                                y + dy:y + dy + self.blockSize // 2]
        return block.mean() if block.size > 0 else 0

    def _get_edge_feature(self, i, j):
        avg = [
            self._get_block_avg(i, j, 0, 0),
            self._get_block_avg(i, j, self.blockSize // 2, 0),
            self._get_block_avg(i, j, 0, self.blockSize // 2),
            self._get_block_avg(i, j, self.blockSize // 2, self.blockSize // 2),
        ]

        edge_filter = np.array([
            [1, -1, 1, -1],
            [1, 1, -1, -1],
            [np.sqrt(2), 0, 0, -np.sqrt(2)],
            [0, np.sqrt(2), -np.sqrt(2), 0],
            [2, -2, -2, 2]
        ])

        strengths = np.abs(np.dot(edge_filter, avg))
        max_strength = strengths.max()
        if max_strength < self.threshold:
            return self.NoEdge
        return np.argmax(strengths) + 1

    def extract_feature(self):
        count_local = [0] * 16

        for y in range(0, self.height - self.blockSize + 1, self.blockSize):
            for x in range(0, self.width - self.blockSize + 1, self.blockSize):
                region_idx = ((x * 4) // self.width) + (((y * 4) // self.height) * 4)
                count_local[region_idx] += 1
                edge_type = self._get_edge_feature(x, y)

                if edge_type != 0:
                    bin_index = region_idx * 5 + [1, 0, 4, 3, 2][edge_type - 1]
                    self.Local_Edge_Histogram[bin_index] += 1

        for k in range(80):
            region = k // 5
            if count_local[region] != 0:
                self.Local_Edge_Histogram[k] /= count_local[region]

        return self.Local_Edge_Histogram

    def quantize(self, histogram):
        result = np.zeros_like(histogram)
        for i, val in enumerate(histogram):
            for j in range(8):
                if j < 7:
                    q = (self.QuantTable[i % 5, j] + self.QuantTable[i % 5, j + 1]) / 2
                else:
                    q = 1.0
                result[i] = j
                if val <= q:
                    break
        return result
