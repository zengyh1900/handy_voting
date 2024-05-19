import argparse
import os

from jinja2 import Template


argparser = argparse.ArgumentParser()
argparser.add_argument("--src", type=str, nargs="+", help="source directories for comparison")
argparser.add_argument("--save_dir", type=str, default="outputs")
argparser.add_argument("--name", type=str, default="exp", help="name of the output file")
args = argparser.parse_args()


def render(template_file="./server/templates/experiment.html"):
    # translate all the path into relative path
    img_list = list(os.listdir(args.src[0]))
    img_list = sorted(img_list)
    source_dirs = [os.path.relpath(sdir, start=args.save_dir) for sdir in args.src]

    # relative path to the style
    style1 = "./server/static/lightbox/css/lightbox.min.css"
    style2 = "./server/static/css/experiment.css"
    style3 = "./server/static/lightbox/js/lightbox-plus-jquery.min.js"
    style1 = os.path.relpath(style1, start=args.save_dir)
    style2 = os.path.relpath(style2, start=args.save_dir)
    style3 = os.path.relpath(style3, start=args.save_dir)

    # write the results
    os.makedirs(args.save_dir, exist_ok=True)

    template = None
    with open(template_file, "r") as f:
        template = Template(f.read())

    output_file = os.path.join(args.save_dir, f"{args.name}.html")
    # timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    # output_file = os.path.join(args.save_dir, f'{timestamp}.html')
    with open(output_file, "w") as f:
        f.write(
            template.render(style1=style1, style2=style2, style3=style3, source_dirs=source_dirs, img_list=img_list)
        )

    print(f"Done. Please check {output_file}.")


if __name__ == "__main__":
    render()
