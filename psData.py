import subprocess
import textfsm
import pandas as pd


def get_process_stats() -> str:
    """Gets all currently running processes and their stats.
    Runs the ps command with the formatted output user, group,
    process id, cpu %, memory %, resident set size, state, start time,
    execution time and command. If the user or group is longer than
    20 characters it is truncated with a '+' and execution time is in seconds.

    Returns
    -------
    str
       a space delimited ascii string
    """
    cmd = "ps axo\
    user:20,group:20,pid,pcpu,pmem,rssize,stat,lstart,etimes,comm".split()
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p1.communicate()[0].decode('ascii')


def parse_process_stats(ps_data: str) -> list:
    """Parses incoming stats string returned from get_process_stats
    Uses textfsm to parse into python list

    Returns
    -------
    list
        a list of lists containing values of ps stats
    """
    data = ps_data
    # knocks off the header entry of data string
    cmdIndex = data.index("COMMAND")
    data = data[cmdIndex+8:]

    with open('ps_template') as f:
        template = textfsm.TextFSM(f)

    results = template.ParseText(data)

    # convert parsed results to appropriate data types
    for row in results:
        row[2] = int(row[2])
        row[3] = float(row[3])
        row[4] = float(row[4])
        row[5] = int(row[5])
        row[9] = int(row[9])
        row[12] = int(row[12])

    return results


def store_process_stats(ps_list: list) -> pd.DataFrame:
    """Creates a pandas dataframe given a list of processes\
    (each process attributes are in list)

    Returns
    -------
    pd.Dataframe
        Pandas dataframe with processes and the corresponding headers
    """
    cols = ['User', 'Group', 'PID', 'CPU', 'MEM', 'RSS', 'STAT',
            'Weekday', 'Month', 'Day', 'Time', 'Year', 'Elapsed', 'Command']
    ps_df = pd.DataFrame(ps_list, columns=cols)
    return ps_df
