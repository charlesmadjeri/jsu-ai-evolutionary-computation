import csv
import os
from datetime import datetime
from PIL import Image

from export.generate_png_export import generate_png_export, save_map

def generate_and_save_csv(result_list:list[tuple[float,float]],total_distance:float,csv_path:str):
        with open(csv_path,mode='w',newline='') as file:
             writer=csv.writer(file)
             writer.writerow(['X','Y'])
             for x,y in result_list:
                 writer.writerow([x, y])
             writer.writerow([])
             writer.writerow(['Total Distance', total_distance])

def generate_and_save_png(result_list:list[tuple[float,float]],image_path:str):
    png_data = generate_png_export(result_list)
    with open(image_path, 'wb') as f:
        f.write(png_data)


def export_results(result_list:list[tuple[float,float]], total_distance:float, export_image:bool = True, export_csv:bool = True):
     if not export_image and not export_csv:
        return
    
     timestamp=datetime.now().strftime('%Y-%m-%d %H-%M-%S')
     result_dir= f'results/simple_passes/{timestamp}'
     os.makedirs(result_dir,exist_ok=True)

     csv_path=os.path.join(result_dir,'results.csv')
     image_path=os.path.join(result_dir,'results.png')

     generate_and_save_csv(result_list, total_distance, csv_path)
     generate_and_save_png(result_list, image_path) 