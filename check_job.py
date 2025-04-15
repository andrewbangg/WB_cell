import win32print


def check_job(name_printer):
    for i in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,
                                     None, 1):
        flags, desc, name, comment = i
        if name_printer in name:
            phandle = win32print.OpenPrinter(name)
            print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
            if len(print_jobs) > 2:
                jobs = len(print_jobs)
                while jobs >= 1:
                    for job in print_jobs:
                        win32print.SetJob(phandle, job['JobId'], win32print.JOB_INFO_1, job,
                                          win32print.JOB_CONTROL_DELETE)
                        jobs = len(win32print.EnumJobs(phandle, 0, -1, 1))
