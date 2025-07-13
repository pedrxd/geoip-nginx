import io
from enum import EnumType
from typing import List

import click
import requests
from click import Choice
from requests import HTTPError

class ListType(EnumType):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"

@click.command()
@click.option('-c', "--countries", type=str, required=True)
@click.option("-o", "--output", type=str, required=False)
@click.option("-t", "--type", type=Choice(["whitelist","blacklist"], case_sensitive=False), required=False, default="whitelist")
def generate(countries: str, output: str, type: ListType):
    countries_list = countries.split(",")

    # Download ip_list
    try:
        ip_list = get_ip_list(countries_list)
    except CountryNotExists as e:
        click.echo(f"Country {e.country} doesn't exist, aborting!")
        exit(-1)

    # Create nginx configuration
    buffer = create_nginx_config(countries_list, ip_list, type)

    # Save the file
    if output is None:
        output = f"{type}.conf"
    save_to_file(buffer, output)


def create_nginx_config(country_list, ip_list, list_type) -> io.StringIO:
    file_to_write = io.StringIO()

    comment = f"##########\n# This is a {list_type} with the following countries: {",".join(country_list)}\n##########\n\n"
    file_to_write.write(comment)

    custom_rule = "allow" if list_type == ListType.WHITELIST else "deny"
    default_rule = "deny all;" if list_type == ListType.WHITELIST else "allow all;"

    for ip in ip_list:
        file_to_write.write(f"{custom_rule} {ip};\n")

    file_to_write.write(f"{default_rule}\n")
    return file_to_write

def save_to_file(buffer: io.StringIO, file_name):
    with open(file_name, "w") as file:
        file.write(buffer.getvalue())


def get_ip_list(country_list: List[str]):
    replace_url = "https://www.ipdeny.com/ipblocks/data/countries/{{country}}.zone"
    ip_list = []
    for country in country_list:
        country_url = replace_url.replace("{{country}}", country)

        try:
            response = requests.get(country_url)
            response.raise_for_status()

            for ip in response.iter_lines():
                ip_list.append(ip.decode("utf-8"))

        except HTTPError as e:
            if e.response.status_code == 404:
                raise CountryNotExist(country)
    return ip_list

class CountryNotExist(Exception):
    def __init__(self, _country):
        self.country = _country
        super()

if __name__ == "__main__":
    generate()
