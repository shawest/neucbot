import sys


class Config:
    def __init__(self, args):
        self.talys = args.get("talys")
        self.download = args.get("download")
        self.force_recalculation = args.get("force_recalculation")
        self.output = (
            open(args.get("output"), "w") if args.get("output") else sys.stdout
        )
