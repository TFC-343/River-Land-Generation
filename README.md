# River-Land-Generation
This here is a small project I made when I first learnt about wave function collapse. <br>
I thought it was cool so gave it a go. <br>
As long as you have pygame and a modern version of python you can just run main.py and create your very own river land. <p>
# Create your own
If you like you can create your own map or whatever else using the algorithm I've written <br>
just upload all your images into the images folder and remove mine <br>
(all my images are 25x25 but as long as yours are square they will be resized correctly). <p>
Then you must tell the program how to connect the tiles, <br>
open helper.py and find my rules on line 14, remove them. <br>
Then create your own rules using the same syntax. <br>
Next, find the function "get_nodes()", this function must return a list of all the possible tiles. <br>
Remove mine and started adding yourown. <br> The function should look like this.
  
```
def get_nodes():
    """returns a list with all nodes"""
    nodes = [
        Node("WaveFunctionCollapse/images/<your_file_name>.png", <north rule>, <east rule>, <south rule>, <west rule>),
        Node("WaveFunctionCollapse/images/<your_second_file_name>.png", <north rule>, <east rule>, <south rule>, <west rule>),
        .
        .
        .
    ]

    return nodes
```
  
 <p>
 Then save the file and rerun main.py to see your own creation.
