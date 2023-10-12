#!/usr/bin/python

from bs4 import BeautifulSoup
from lxml import etree
from csv import DictWriter
from os.path import exists
import datefinder
from datetime import date
import os
import re


def main():
    fields = ["posted_date", "posted_time", "description", "time", "date"]

    directory = "messages"

    file = "messages.csv"

    for filename in os.scandir(directory):
        print("------------------------------")
        print(f"Scraping: {filename.path}")
        print("------------------------------")
        file_exists(fields, file)

        with open(filename.path, "r") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, "lxml")
            dom = etree.HTML(str(soup))

        messages = dom.xpath(
            "//div[@class='history']/div[contains (@class, 'message default clearfix')]"
        )

        for count, _ in enumerate(messages, start=1):
            posted_date = ""
            posted_time = ""
            description = ""
            time = ""
            real_date = ""

            text_clean = []

            text_raw = dom.xpath(
                f"//div[@class='history']/div[contains (@class, 'message default clearfix')][{count}]//div[@class='text']//text()"
            )

            removed = remove(text_raw)

            for text in removed:
                text_clean.append(text.strip().replace("\n", "").replace("  ", ""))

            description = " ".join(text_clean)

            posted_date, posted_time, _ = dom.xpath(
                f"//div[@class='history']/div[contains (@class, 'message default clearfix')][{count}]//div[@class='pull_right date details']/@title"
            )[0].split(" ")

            if text_clean:
                real_date_time = text_clean.pop(-1)

                dates_times = datefinder.find_dates(real_date_time)
                for date_time in dates_times:
                    try:
                        real_date, time = str(date_time).split(" ")
                    except ValueError:
                        pass

            if description:
                messages = {
                    "posted_date": posted_date,
                    "posted_time": posted_time,
                    "description": description,
                    "time": time,
                }
                if not real_date == str(date.today()) and not real_date == "1900-01-31":
                    messages["date"] = real_date

            write_to_csv(fields, file, messages)


def file_exists(fields, file):
    if not exists(file):
        with open(file, "w") as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=fields)
            dictwriter_object.writeheader()


def write_to_csv(fields, file, messages):
    with open(file, "a") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=fields)
        dictwriter_object.writerow(messages)
        return True


def remove(text_raw):
    if "\n" in text_raw:
        text_raw.remove("\n")
    if "" in text_raw:
        text_raw.remove("")
    if "#EAR" in text_raw:
        text_raw.remove("#EAR")
    return text_raw


if __name__ == "__main__":
    main()
