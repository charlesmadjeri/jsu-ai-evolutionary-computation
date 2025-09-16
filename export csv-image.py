import csv
import os
from datetime import datetime
from typing import List,Tuple,Any
from PIL import Image
import matplotlib.pyplot as plt
import math

def export_results(result_list:List[Tuple[float,float],result_image: Any])
    #create results directory
    os.makedirs('results', exist_ok=True)
    #Generate timestamped filename
    timestamp=datetime.now().strftime('%Y-%m-%d %H %M %S')
    csv_filename= f'results/{timestamp}.csv'
    image_filename=f'results/{timestamp}.png'

    #calculate total distance
    total_distance=0.0
    for i in range(1,len(result_list)):
        x1,y1=result_list[i-1]
        x2,y2=result_list[i]
        total_distance += math.hypot(x2-x1,y2-y1)
    #Write CSV file with coordinates and total distance
    with open(csv_filename,mode='w',newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['X','Y'])
        for x,y in result_list:
            writer.writerow([x,y])
            writer.writerow(['Total Distance', total_distance])

    #Create Visualization and save image
    x_coords, y_coords=zip(*result_list)
    plt.figure(figsize=(8,6))
    plt.plot(x_coords, y_coords,marker='o')
    plt.title('Coordinate Visualization')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.savefig(image_filename)
    plt.close()

    #Save the result_image if a PIL Image
    if isinstance(result_image,Image.Image)
    result_image.save(image_filename)
    return csv_filename,image_filename
