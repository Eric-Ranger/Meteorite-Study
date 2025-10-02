import argparse
from .config import Settings
from .steps.load_raw import LoadRawETL
from .steps.geocode import GeocodeETL
from .steps.normalize import NormalizeETL
from .steps.export_json import ExportJson

def main():
    parser = argparse.ArgumentParser(prog="meteorite_pipeline", description="Meteorite JSON pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run a pipeline step")
    run_p.add_argument("step", choices=["all", "load-raw", "geocode", "normalize", "export"])

    # optional overrides
    run_p.add_argument("--raw-db")
    run_p.add_argument("--loc-db")
    run_p.add_argument("--dw-db")
    run_p.add_argument("--output")

    args = parser.parse_args()
    s = Settings()

    if args.raw_db: s.raw_db = args.raw_db
    if args.loc_db: s.loc_db = args.loc_db
    if args.dw_db: s.dw_db = args.dw_db
    if args.output: s.output_json = args.output

    if args.step in ("all", "load-raw"):
        LoadRawETL(s).run()
    if args.step in ("all", "geocode"):
        GeocodeETL(s).run()
    if args.step in ("all", "normalize"):
        NormalizeETL(s).run()
    if args.step in ("all", "export"):
        ExportJson(s).run()

if __name__ == "__main__":
    main()