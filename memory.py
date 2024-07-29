import tkinter as tk
import math
import random
from tkinter import messagebox

def update_checkboxes():
    if var_l1.get():
        checkbox_l2.config(state=tk.NORMAL)
    else:
        var_l2.set(0)
        var_l3.set(0)
        checkbox_l2.config(state=tk.DISABLED)
        checkbox_l3.config(state=tk.DISABLED)
    
    if var_l2.get():
        checkbox_l3.config(state=tk.NORMAL)
    else:
        var_l3.set(0)
        checkbox_l3.config(state=tk.DISABLED)

def show_selected():
    selected_options = []
    if var_l1.get():
        selected_options.append("Cache L1")
    if var_l2.get():
        selected_options.append("Cache L2")
    if var_l3.get():
        selected_options.append("Cache L3")
    
    root.withdraw()
    initialize_caches(selected_options)

def initialize_caches(selected_options):
    def is_power_of_two(n):
        return (n & (n - 1) == 0) and n != 0

    def save_initial_values():
        try:
            cache_values = {}
            block_sizes = {}
            access_times = {}
            cache_arrays = {}
            R_array={}
            access={}
            hit={}
            
           
            

            for option in selected_options:
                size = int(entry_values[option].get())
                block_size = int(block_size_entries[option].get())
                access_time = int(access_time_entries[option].get())
                
                
                
                if not is_power_of_two(block_size):
                    raise ValueError(f"{option} Number of Blocks must be power of 2")

                cache_values[option] = size
                block_sizes[option] = block_size
                access_times[option] = access_time
                cache_arrays[option] = [[{"valid_bit": 0, "tag": "--", "data": "--"} for _ in range(2)] for _ in range(block_size)]
                R_array[option]=[0]*block_size
                access[option]=0
                hit[option]=0


            dram_value = int(entry_dram.get())
            virtual_memory_value = int(entry_virtual_memory.get())
            disk_value = int(entry_disk.get())

            # Validation for the values
            if "Cache L1" in cache_values and "Cache L2" in cache_values:
                if cache_values["Cache L1"] >= cache_values["Cache L2"]:
                    raise ValueError("Cache L1 size must be less than Cache L2 size")
            if "Cache L2" in cache_values and "Cache L3" in cache_values:
                if cache_values["Cache L2"] >= cache_values["Cache L3"]*1000:
                    raise ValueError("Cache L2 size must be less than Cache L3 size")
            if "Cache L3" in cache_values:
                if cache_values["Cache L3"] >= dram_value*1000:
                    raise ValueError("Cache L3 size must be less than Dram size")
            if "Cache L2" in cache_values:
                if cache_values["Cache L2"] >= dram_value*1000000:
                    raise ValueError("Cache L2 size must be less than Dram size")
            if "Cache L1" in cache_values:
                if cache_values["Cache L1"] >= dram_value*1000000:
                    raise ValueError("Cache L1 size must be less than Dram size")
            if dram_value >= disk_value:
                raise ValueError("Dram size must be less than Disk size")
            if dram_value >= virtual_memory_value:
                raise ValueError("Dram size must be less than virtual memory size")

            if virtual_memory_value >= disk_value:
                raise ValueError("Virtual Memory size must be less than Disk size")

            # Display selected options and values
            message = "Selected Caches with Values:\n"
            for option in cache_values:
                if option !="Cache L3":
                    message += f"{option}: {cache_values[option]} KB, Number of Blocks : {block_sizes[option]}, Access Time: {access_times[option]} ms\n"
                if option =="Cache L3":
                    message += f"{option}: {cache_values[option]} MB, Number of Blocks : {block_sizes[option]}, Access Time: {access_times[option]} ms\n"


            message += f"Dram: {dram_value} GB\n"
            message += f"Virtual Memory: {virtual_memory_value} GB\n"
            message += f"Disk: {disk_value} GB\n"
            messagebox.showinfo("Selected Caches with Values", message)

            # Close the initialization window
            initialization_window.destroy()
             
            virtual_memory_value *= (2**28)
            virtual_address_bit = math.ceil(math.log2(virtual_memory_value))

            dram_value *= (2**28)
            memory_address_bit = math.ceil(math.log2(dram_value))
            
            # Open new window to select cache implementation policy
            select_policy_window(memory_address_bit, block_sizes,cache_arrays,R_array,access,hit)
            
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def select_policy_window(memory_address_bit, block_sizes,cache_arrays,R_array,access,hit):
        def on_policy_select():
            selected_policy = policy_var.get()
            policy_window.destroy()
            generate_hex_window(memory_address_bit, block_sizes,cache_arrays,selected_policy,R_array,access,hit)

        policy_window = tk.Toplevel(root)
        policy_window.title("Select Cache Implementation Policy")
        policy_window.geometry("400x300")

        policy_var = tk.StringVar()
        policy_var.set("Random")  # Default policy

        label = tk.Label(policy_window, text="Select Cache Implementation Policy", font=("Arial", 14))
        label.pack(pady=20)

        radio_random = tk.Radiobutton(policy_window, text="Random", variable=policy_var, value="Random", font=("Arial", 12))
        radio_random.pack(anchor='w', padx=20, pady=5)
        
        radio_lru = tk.Radiobutton(policy_window, text="LRU", variable=policy_var, value="LRU", font=("Arial", 12))
        radio_lru.pack(anchor='w', padx=20, pady=5)
        
        radio_fifo = tk.Radiobutton(policy_window, text="FIFO", variable=policy_var, value="FIFO", font=("Arial", 12))
        radio_fifo.pack(anchor='w', padx=20, pady=5)

        select_button = tk.Button(policy_window, text="Select Policy", command=on_policy_select, font=("Arial", 14), bg="lightgreen")
        select_button.pack(pady=20)
    def generate_hex_window(memory_address_bit, block_sizes, cache_arrays,selected_policy,R_array,access,hit):
        def generate_hex():
            max_value = 2 ** memory_address_bit - 1
            random_hex = hex(random.randint(0, max_value))
            used_addresses.add(random_hex)
            hex_display_label.config(text=random_hex)
            binary_str = hex_to_bin(random_hex)
            binary_display_label.config(text=binary_str)

            display_tables(block_sizes,cache_arrays,R_array)
            simulate_cache_behavior(binary_str,R_array,access,hit) 


           
        
        

        def enter_hex():
            entered_hex = hex_entry.get()
            try:
                entered_value = int(entered_hex, 16)
                if entered_value < 0 or entered_value >= 2 ** memory_address_bit:
                    raise ValueError("Hexadecimal number out of range")
                used_addresses.add(entered_hex)
                hex_display_label.config(text=entered_hex)
                
                binary_str = int_to_binary(entered_value)
                binary_display_label.config(text=binary_str)
                display_tables(block_sizes,cache_arrays,R_array)
                simulate_cache_behavior(binary_str,R_array,access,hit)
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
        def int_to_binary(n):
   
            return bin(n)[2:]  

        def hex_to_bin(hex_string):
   
            try:
                    # Convert the hexadecimal string to an integer
                decimal_value = int(hex_string, 16)
                    
                    # Convert the integer to a binary string, remove the '0b' prefix
                binary_string = bin(decimal_value)[2:]
                    
                return binary_string
            except ValueError:
                return "Invalid hexadecimal input"
            

        
        def create_table_frame(parent, cache_name, frame_width, frame_height):
            frame = tk.Frame(parent, bd=2, relief=tk.RIDGE, padx=5, pady=5, width=frame_width, height=frame_height)
            frame.grid_propagate(False)
            
            label = tk.Label(frame, text=cache_name, font=("Arial", 12, "bold"))
            label.grid(row=0, column=0, columnspan=6, pady=5)
            
            canvas = tk.Canvas(frame)
            canvas.grid(row=1, column=0, columnspan=6, sticky=tk.NSEW)
            
            v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
            v_scrollbar.grid(row=1, column=6, sticky=tk.NS)
            
            h_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
            h_scrollbar.grid(row=2, column=0, columnspan=6, sticky=tk.EW)
            
            canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
            
            inner_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)
            
            return frame, canvas, inner_frame

        def display_tables(block_sizes, cache_arrays, R_array):
            table_window = tk.Toplevel()
            table_window.title("Cache Tables")

            num_caches = len(cache_arrays)
            window_width = 800 + (num_caches - 1) * 200
            window_height = 600
            table_window.geometry(f"{window_width}x{window_height}")

            cache_order = ["Cache L1", "Cache L2", "Cache L3"]
            frame_width = 400
            frame_height = 500

            for idx, cache_name in enumerate(cache_order):
                if cache_name not in block_sizes:
                    continue

                frame, canvas, inner_frame = create_table_frame(table_window, cache_name, frame_width, frame_height)
                frame.grid(row=0, column=idx, padx=10, pady=5, sticky="nsew")
                
                if selected_policy == "LRU":
                    col_names = ["Block Number", "R", "Valid Bit", "Tag", "Data", "Valid Bit", "Tag", "Data"]
                else:
                    col_names = ["Block Number", "Valid Bit", "Tag", "Data", "Valid Bit", "Tag", "Data"]

                for col, col_name in enumerate(col_names):
                    header = tk.Label(inner_frame, text=col_name, font=("Arial", 12, "bold"))
                    header.grid(row=0, column=col, padx=5, pady=5)

                for set_idx, cache_set in enumerate(cache_arrays[cache_name]):
                    if selected_policy == "LRU":
                        tk.Label(inner_frame, text=R_array[option][set_idx], font=("Arial", 12)).grid(row=set_idx + 1, column=1, padx=5, pady=5)
                    
                    for line_idx, cache_line in enumerate(cache_set):
                        tk.Label(inner_frame, text=set_idx, font=("Arial", 12)).grid(row=set_idx + 1, column=0, padx=5, pady=5)
                        
                        if selected_policy == "LRU":
                            tk.Label(inner_frame, text=cache_line["valid_bit"], font=("Arial", 12)).grid(row=set_idx + 1, column=line_idx * 3 + 2, padx=5, pady=5)
                            tk.Label(inner_frame, text=cache_line["tag"], font=("Arial", 12)).grid(row=set_idx + 1, column=line_idx * 3 + 3, padx=5, pady=5)
                            tk.Label(inner_frame, text=cache_line["data"], font=("Arial", 12)).grid(row=set_idx + 1, column=line_idx * 3 + 4, padx=5, pady=5)
                        else:
                            tk.Label(inner_frame, text=cache_line["valid_bit"], font=("Arial", 12)).grid(row=set_idx + 1, column=line_idx * 3 + 1, padx=5, pady=5)
                            tk.Label(inner_frame, text=cache_line["tag"], font=("Arial", 12)).grid(row=set_idx + 1, column=line_idx * 3 + 2, padx=5, pady=5)
                            tk.Label(inner_frame, text=cache_line["data"], font=("Arial", 12)).grid(row=set_idx + 1, column=line_idx * 3 + 3, padx=5, pady=5)

                inner_frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
                



        def simulate_cache_behavior(binary_st,R_array,access,hit):
            
            
            
            for option in selected_options:
                
                index=set_index(binary_st,option)
                tag=set_tag(binary_st,option)
                line= binary_to_decimal(index)
                status=set_status(option,line,tag,R_array)

                access[option]+=1
                if status=="hit":
                    hit[option]+=1

                hit_rate = hit[option] /access[option]    
                miss_rate=1-hit_rate
                print(option+":")
                print(f"Hit Rate: {hit_rate * 100:.2f}%")
                print(f"Miss Rate: {miss_rate * 100:.2f}%\n")


                index_labels[option].config(text=f"Index:{index}")
                tag_labels[option].config(text=f"Tag: {tag}")
                status_labels[option].config(text=f"Status:{status}")
            print("----------------")
                           
            

        def binary_to_decimal(binary_str):
    
            try:
                # Convert binary string to decimal integer using int with base 2
                decimal_value = int(binary_str, 2)
                return decimal_value
            except ValueError:
                # Handle the case where the input is not a valid binary string
                print("Invalid binary input")
                return None
        used_addresses = set()

        hex_window = tk.Toplevel()
        hex_window.title("Generate Hexadecimal Number")
        hex_window.geometry("600x400")

        left_frame = tk.Frame(hex_window, width=400, height=400, bd=1, relief=tk.SOLID)
        left_frame.pack_propagate(False)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        label = tk.Label(left_frame, text="Generate or Enter Hexadecimal Number", font=("Arial", 14))
        label.pack(pady=20)

        generate_button = tk.Button(left_frame, text="Generate Hex", command=generate_hex, font=("Arial", 12), bg="lightblue")
        generate_button.pack(pady=10)

        or_label = tk.Label(left_frame, text="OR", font=("Arial", 12))
        or_label.pack(pady=5)

        hex_entry = tk.Entry(left_frame, font=("Arial", 12))
        hex_entry.pack(pady=5)

        enter_button = tk.Button(left_frame, text="Enter Hex", command=enter_hex, font=("Arial", 12), bg="lightgreen")
        enter_button.pack(pady=10)

        hex_display_label = tk.Label(left_frame, text="", font=("Arial", 14, "bold"))
        hex_display_label.pack(pady=20)

        binary_display_label = tk.Label(left_frame, text="", font=("Arial", 14, "bold"))
        binary_display_label.pack(pady=20)

        right_frame = tk.Frame(hex_window, width=300, height=800, bd=1, relief=tk.SOLID)
        right_frame.pack_propagate(False)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)


        

       

        index_labels = {}
        tag_labels = {}
        status_labels = {}
        

        # Display initial caches if any are predefined
        for cache_name in selected_options:
            label_cache = tk.Label(right_frame, text=f"{cache_name}", font=("Arial", 14, "bold"))
            label_cache.pack(pady=20)

            index_label = tk.Label(right_frame, text=f"Index: ", font=("Arial", 12))
            index_label.pack()

            tag_label = tk.Label(right_frame, text=f"Tag: ", font=("Arial", 12))
            tag_label.pack()

            status_label = tk.Label(right_frame, text=f"Status: ", font=("Arial", 12))
            status_label.pack()

            

           
            index_labels[cache_name] = index_label
            tag_labels[cache_name] = tag_label
            status_labels[cache_name] = status_label
            

            def set_index(binary,cache):
                bit_of_index=math.ceil(math.log2(block_sizes[cache]))
                return binary[-bit_of_index:]
            def set_tag(binary,cache):
                bit_of_index=math.ceil(math.log2(block_sizes[cache]))
                return binary[:-bit_of_index]
            def set_status(option,index,tag,R_array):
                cache_line=cache_arrays[option][index]
                cache_line1=cache_arrays[option][index][0]
                cache_line2=cache_arrays[option][index][1]
                
                if cache_line1["tag"]==tag and cache_line1["valid_bit"]==1:
                    if selected_policy=="LRU":
                        R_array[option][index]=0
                    return "hit"
                if cache_line2["tag"]==tag and cache_line2["valid_bit"]==1:
                    if selected_policy=="LRU":
                        R_array[option][index]=1
                    return "hit"
                else:
                    
                    if cache_line1["valid_bit"]==0:
                        cache_line1["tag"]=tag 
                        cache_line1["valid_bit"]=1
                        cache_line1["data"]="data"
                        if selected_policy=="LRU" or selected_policy=="FIFO":
                            
                            R_array[option][index]=0
                        
                        return "miss"


                    if cache_line2["valid_bit"]==0:
                        cache_line2["tag"]=tag 
                        cache_line2["valid_bit"]=1
                        cache_line2["data"]="data"
                        if selected_policy=="LRU" or selected_policy=="FIFO":
                            
                            R_array[option][index]=1
                        return "miss"

                    else:
                        if selected_policy=="Random":
                            lset=random.randint(0,1)
                            cache_line[lset]["tag"]=tag
                            cache_line[lset]["valid_bit"]=1
                            cache_line[lset]["data"]="data"
                            return "miss"
                        if selected_policy=="LRU" or selected_policy=="FIFO":
                        
                            if R_array[option][index]==0:
                                cache_line[1]["tag"]=tag
                                cache_line[1]["valid_bit"]=1
                                cache_line[1]["data"]="data"
                                R_array[option][index]=1
                                return "miss"
                            if R_array[option][index]==1:
                                cache_line[0]["tag"]=tag
                                cache_line[0]["valid_bit"]=1
                                cache_line[0]["data"]="data"
                                R_array[option][index]=0
                                return "miss"
                            
                        

                            


                        
 
                    
                    # return "miss"
                

    initialization_window = tk.Toplevel(root)
    initialization_window.title("Initialize Caches")
    initialization_window.geometry("400x600")

    label = tk.Label(initialization_window, text="Initialize Caches", font=("Arial", 14))
    label.pack(pady=10)

    entry_values = {}
    block_size_entries = {}
    access_time_entries = {}

    for option in selected_options:
        frame = tk.Frame(initialization_window)
        frame.pack(pady=5)
        print(option)


        if option!="Cache L3":
            label = tk.Label(frame, text=f"{option} Size (KB):", font=("Arial", 12))
            label.grid(row=0, column=0, padx=5)
        if option=="Cache L3":
            label = tk.Label(frame, text=f"{option} Size (MB):", font=("Arial", 12))
            label.grid(row=0, column=0, padx=5)


        entry = tk.Entry(frame, font=("Arial", 12))
        entry.grid(row=0, column=1, padx=5)
        entry_values[option] = entry

        label_block = tk.Label(frame, text=f"Number of Blocks {option}:", font=("Arial", 12))
        label_block.grid(row=1, column=0, padx=5)

        block_entry = tk.Entry(frame, font=("Arial", 12))
        block_entry.grid(row=1, column=1, padx=5)
        block_size_entries[option] = block_entry

        label_time = tk.Label(frame, text=f"Access Time (ms) {option}:", font=("Arial", 12))
        label_time.grid(row=2, column=0, padx=5)

        time_entry = tk.Entry(frame, font=("Arial", 12))
        time_entry.grid(row=2, column=1, padx=5)
        access_time_entries[option] = time_entry

    label_dram = tk.Label(initialization_window, text="Dram (GB):", font=("Arial", 12))
    label_dram.pack(pady=5)
    entry_dram = tk.Entry(initialization_window, font=("Arial", 12))
    entry_dram.pack(pady=5)

    label_virtual_memory = tk.Label(initialization_window, text="Virtual Memory (GB):", font=("Arial", 12))
    label_virtual_memory.pack(pady=5)
    entry_virtual_memory = tk.Entry(initialization_window, font=("Arial", 12))
    entry_virtual_memory.pack(pady=5)

    label_disk = tk.Label(initialization_window, text="Disk (GB):", font=("Arial", 12))
    label_disk.pack(pady=5)
    entry_disk = tk.Entry(initialization_window, font=("Arial", 12))
    entry_disk.pack(pady=5)

    save_button = tk.Button(initialization_window, text="Save Values", command=save_initial_values, font=("Arial", 14), bg="lightgreen")
    save_button.pack(pady=20)

root = tk.Tk()
root.title("Cache Selection")
root.geometry("400x400")

label = tk.Label(root, text="Select Cache Levels", font=("Arial", 14))
label.pack(pady=20)

var_l1 = tk.IntVar()
var_l2 = tk.IntVar()
var_l3 = tk.IntVar()

checkbox_l1 = tk.Checkbutton(root, text="Cache L1", variable=var_l1, font=("Arial", 12), command=update_checkboxes)
checkbox_l1.pack(anchor='w', padx=20, pady=5)

checkbox_l2 = tk.Checkbutton(root, text="Cache L2", variable=var_l2, font=("Arial", 12), command=update_checkboxes, state=tk.DISABLED)
checkbox_l2.pack(anchor='w', padx=20, pady=5)

checkbox_l3 = tk.Checkbutton(root, text="Cache L3", variable=var_l3, font=("Arial", 12), state=tk.DISABLED)
checkbox_l3.pack(anchor='w', padx=20, pady=5)

show_button = tk.Button(root, text="Show Selected", command=show_selected, font=("Arial", 14), bg="lightgreen")
show_button.pack(pady=20)

root.mainloop()
