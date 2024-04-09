import tkinter as tk
from tkinter import ttk

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.priority = priority

def calculate_waiting_time(processes):
    total_time = 0
    for process in processes:
        total_time += process.burst_time
        process.turnaround_time = total_time
        process.waiting_time = total_time - process.burst_time - process.arrival_time

def fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)
    calculate_waiting_time(processes)

def sjf(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    calculate_waiting_time(processes)

def srt(processes):
    time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        remaining_processes.sort(key=lambda x: (x.remaining_time, x.arrival_time))
        shortest_process = remaining_processes[0]
        if shortest_process.arrival_time > time:
            time = shortest_process.arrival_time
        shortest_process.remaining_time -= 1
        time += 1
        if shortest_process.remaining_time == 0:
            remaining_processes.remove(shortest_process)
            shortest_process.waiting_time = time - shortest_process.burst_time - shortest_process.arrival_time

def priority(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))
    calculate_waiting_time(processes)

def round_robin(processes, quantum):
    time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        for process in remaining_processes:
            if process.remaining_time > 0:
                if process.remaining_time > quantum:
                    time += quantum
                    process.remaining_time -= quantum
                else:
                    time += process.remaining_time
                    process.waiting_time = time - process.burst_time - process.arrival_time
                    process.remaining_time = 0
        remaining_processes = [p for p in remaining_processes if p.remaining_time > 0]

def print_results(processes):
    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)

    output_text = "Process\tWaiting Time\tTurnaround Time\n"
    for process in processes:
        output_text += f"{process.pid}\t{process.waiting_time}\t\t{process.turnaround_time}\n"
    output_text += f"\nAverage Waiting Time: {avg_waiting_time}\n"
    output_text += f"Average Turnaround Time: {avg_turnaround_time}\n"

    result_text.set(output_text)

def submit_processes():
    processes = []
    for i in range(int(num_processes_entry.get())):
        pid = i + 1
        arrival_time = int(arrival_entries[i].get())
        burst_time = int(burst_entries[i].get())
        priority_value = int(priority_entries[i].get())
        processes.append(Process(pid, arrival_time, burst_time, priority_value))

    if scheduling_algorithm.get() == "FCFS":
        fcfs(processes)
    elif scheduling_algorithm.get() == "SJF":
        sjf(processes)
    elif scheduling_algorithm.get() == "SRTN":
        srt(processes)
    elif scheduling_algorithm.get() == "Priority":
        priority(processes)
    elif scheduling_algorithm.get() == "Round Robin":
        quantum = int(quantum_entry.get())
        round_robin(processes, quantum)

    print_results(processes)

def update_process_entries():
    for entry in arrival_entries + burst_entries + priority_entries:
        entry.grid_forget()

    arrival_entries.clear()
    burst_entries.clear()
    priority_entries.clear()

    for i in range(int(num_processes_entry.get())):
        arrival_entry = ttk.Entry(main_frame)
        arrival_entry.grid(row=i + 4, column=0, padx=10, pady=5)
        arrival_entries.append(arrival_entry)

        burst_entry = ttk.Entry(main_frame)
        burst_entry.grid(row=i + 4, column=1, padx=10, pady=5)
        burst_entries.append(burst_entry)

        priority_entry = ttk.Entry(main_frame)
        priority_entry.grid(row=i + 4, column=2, padx=10, pady=5)
        priority_entries.append(priority_entry)
