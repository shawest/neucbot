import sys
import shutil


class Config:
    def __init__(self, args):
        self.talys = args.get("talys")
        self.download = args.get("download")
        self.force_recalculation = args.get("force_recalculation")
        self.data_source = args.get("data_source")
        self.output = (
            open(args.get("output"), "w") if args.get("output") else sys.stdout
        )
        self.json = args.get("json")

    def validate(self):
        # Return True if TALYS is not being run
        if not (self.talys or self.force_recalculation):
            return

        # Raise a RuntimeError if attempting to use data_source = slim with
        # either --talys or --force-recalculation. Opting to use preprocessed
        # data does not allow for TALYS calculations
        if self.data_source == "slim":
            raise RuntimeError(
                "Attempting to run TALYS while using preprocessed data. Please rerun without --talys or --force-recalculation."
            )

        # If TALYS is being run, verify that the talys command is present
        if shutil.which("talys"):
            return
        else:
            raise RuntimeError(
                "Attempting to run TALYS when talys command is not available"
            )
