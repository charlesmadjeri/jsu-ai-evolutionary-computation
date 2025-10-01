import csv
import os
from datetime import datetime
from typing import List,Tuple,Any
from PIL import Image
import math

def compute_distances(result_list:List[Tuple[float,float]])->float:
    total_distance= 0.0
    for i in range(1,len(result_list)):
        x1,y1= result_list[i-1]
        x2,y2= result_list[i]
        total_distance +=math.hypot(x2-x1, y2-y1)
        return total_distance
    
def generate_csv_export(result_list:List[Tuple[float,float]],
    total_distance:float,csv_path:str):
        with open(csv_path,mode='w',newline='') as file:
             writer=csv.writer(file)
             writer.writerow(['X','Y'])
             for x,y in result_list:
                  writer.writerow(['Total Distance', total_distance])

def generate_png_export(result_list:List[Tuple[float,float]],result_image:Any,image_path:str):
     

     if isinstance(result_image,Image.Image):
        result_image.save(image_path)

def export_results(result_list:List[Tuple[float,float]],result_image:Any):
     timestamp=datetime.now().strftime('%Y-%m-%d %H-%M-%S')
     result_dir= f'results/{timestamp}'
     os.makedirs(result_dir,exist_ok=True)

     csv_path=os.path.join(result_dir,'results.csv')
     image_path=os.path.join(result_dir,'results.png')

     total_distance=compute_distances(result_list)

   ###  generate_csv_export(result_list,total_distance,csv_path)

    # generate_png_export(result_list,result_image,image_path)
      
     return csv_path,image_path ###



