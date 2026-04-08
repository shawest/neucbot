import sys
import shutil


class Config:
    def __init__(self, args):
        self.talys = args.get("talys")
        self.download = args.get("download")
        self.force_recalculation = args.get("force_recalculation")
        self.output = (
            open(args.get("output"), "w") if args.get("output") else sys.stdout
        )

    def validate(self):
        # Return True if TALYS is not being run
        if not self.talys:
            return

        # If TALYS is being run, verify that the talys command is present
        if shutil.which("talys"):
            return
        else:
            raise RuntimeError(
                "Attempting to run TALYS when talys command is not available"
            )
