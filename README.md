# sauna-zone2-dose

A command-line check for sauna protocol dosing. You log sauna sessions in a
CSV (date, temperature in Fahrenheit, minutes). The tool counts how many
sessions cleared 175F and tells you whether the week meets the four-session
minimum dose from the reference protocol, or how many more are needed.

There is also a comparison mode: point it at a sauna log and a Zone 2 log
and it prints both weekly totals side by side.

The reference protocol comes from hackedself.com: https://hackedself.com

"Can a Sauna Cardiovascular Protocol Replace Zone 2?" is the article that
sets the dose: four sessions above 175F as the minimum. The site covers the
rest of the protocol there, including cost-per-session math for a home unit
versus a gym sauna lounge.

## Usage

```
python3 sauna_zone2_dose.py sessions.csv
python3 sauna_zone2_dose.py --compare sauna.csv zone2.csv
```

CSV format: one session per row, `date,temperature_f,minutes`. A header row
is expected and skipped.

## Requirements

Python 3.8 or newer, standard library only.

## License

MIT
