from .base_options import BaseOptions


class TestOptions(BaseOptions):
    def initialize(self, parser):
        parser = BaseOptions.initialize(self, parser)
        parser.add_argument("--image", type=str, default='')
        parser.add_argument("--result", type=str, default='', help='path to the .nii result to save')
        parser.add_argument('--phase', type=str, default='test', help='test')
        parser.add_argument('--which_epoch', type=str, default='20', help='which epoch to load? set to latest to use latest cached model')
        parser.add_argument("--stride_inplane", type=int, nargs=1, default=8, help="Stride size in 2D plane")
        parser.add_argument("--stride_layer", type=int, nargs=1, default=8, help="Stride size in z direction")

        # parser.set_defaults(model='test')
        # parser.set_defaults(model='condition_test')
        self.isTrain = False
        return parser