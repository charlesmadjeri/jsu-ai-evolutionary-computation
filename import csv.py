import csv
from io import StringIO
from typing import List,Tuple,any
from PIL import Image

def process_results(result_list:List[Tuple[float,float]],result_image: any) -> str:

    output= StringIO()
    writer= csv.writer(output)

    #write header
    writer.writerow(['x','y'])

    #write data rows
    for x,y in result_list:
        writer.writerow([x,y])



#Export results
csv_path,image_path=export_results(result_list,result_image)
print(f"CSV saved to: {csv_path}")
print(f"Image saved to {image_path}")