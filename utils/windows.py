import pygetwindow as gw


def list_holdem_windows():
    windows = gw.getAllWindows()
    holdem_windows = [window for window in windows if "RuneLite" in window.title]

    holdem_table_info = []

    for window in holdem_windows:
        handle = window._hWnd
        title = window.title
        table_name = title.split(' -')[0]  # Extract table name
        print(f"Handle: {handle}, Table Name: {table_name}")
        holdem_table_info.append((handle, table_name))

    return holdem_table_info


if __name__ == "__main__":
    table_info = list_holdem_windows()
    # table_info now contains a list of (handle, table_name) tuples
    for handle, table_name in table_info:
        print(f"Returned Handle: {handle}, Table Name: {table_name}")
