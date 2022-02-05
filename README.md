# Kraftringen Exporter
### Export metrics from Kraftringen's portal
***

### Setting up

##### Quickstart

Run the login command and point it to a file you'd like to save your cookies to.

```shell
python3 -m main -- login > cookies.txt
```

Scan the QR code printed in the terminal with your Mobile BankID app.

```text
█▀▀▀▀▀█   ▀█▀█▄▄▀  ▀█ █▀▀▀▀▀█
█ ███ █ █▀██▄▄█▄▀▄▄█▀ █ ███ █
█ ▀▀▀ █ █▄ █ ▄▀▄▀▄▀▀█ █ ▀▀▀ █
▀▀▀▀▀▀▀ █ █▄▀ ▀▄▀ ▀ ▀ ▀▀▀▀▀▀▀
▀▄█▀██▀ ▄▀▄█ ▄ ▀ ▀ ██ ███▀▀ ▄
▀█ ▄ ▀▀█ █▄▄▄█▀▀█▀█  ▄  █▀▀  
█▄▀▀  ▀▀█ █▀▄ ▀▀▄▀▄▄ ▄▄ ▄ ▀██
▄▄ ▄▄▀▀ █▄▀▀▄ ▄▀▄   ▄█▀▄█▄ ▄ 
█▀  ▀▄▀ ▄ ▄ ▄▄▄ ▄▀██▄▄▄█▄ ███
█ █▀▄▄▀▄▄▀ ▀▄█▀█▀ █▄   █ █ ▄ 
▀  ▀ ▀▀ ▄██▄█ ▀ ▄█▄▄█▀▀▀█▀▀ ▄
█▀▀▀▀▀█ ▄  ▀▀ ▄▀▀ ▄██ ▀ █▀▀▄▄
█ ███ █ ███ ▄ ▄ ▄█▄▄▀█▀▀▀ ▀▄▄
█ ▀▀▀ █ ▀█ ▀▀▀ ▀█▀ █▄█▀▀▀▄ █ 
▀▀▀▀▀▀▀ ▀ ▀  ▀▀  ▀ ▀ ▀ ▀  ▀  
```

Use the cookies to curl further, authorized resources.

```shell
curl -b cookies.txt "https://mittkraftringen.kraftringen.se/api/resources/consumption.aspx/specific/Page_Title/"
```

### Documentation

For now, refer to the source.

### Contributing

Any contribution is welcome. If you're not able to code it yourself, perhaps someone else is - so post an issue if there's anything on your mind.

###### Development

Clone the repository:
```shell
git clone https://github.com/AlexGustafsson/kraftringen-exporter
```

Setup a virtual environment and dependencies:
```shell
make setup
```

Write code and commit it.

Follow the conventions enforced:
```shell
make static-analysis
```

Test the project:
```shell
make test
```
