# kEvol

kEvol is a multi-program family that has implemented EA algorithms.

## Description


kEvol is a multi-program family that has been written in Python. You can use this family, whether as a single set of programs or modules imported in other programs. kEvol allows to define all the possible values of the EA algorithm's parameters and create all possible combinations of those parameters known as the configurations. The algorithm will test these configurations, and a report will be generated. A command line-based reporter also allows users to load the EA algorithm report(s) and query different information and plot them.


## Getting Started

### Dependencies

* OS: Windows/Linux
* Python3.8 or later

### Installing


* Currently, the only support is for the \*nix-based systems
* Currently, the only support is for the execuatble files not library files


To install simply
```
   $ git clone https://github.com/keagleV/kEvol.git
   $ cd kEvol
   $ echo  PATH=$PATH:$PWD >>  $HOME/.bashrc
   $ cd dist
   $ pip3 install kEvol-1.0.tar.gz
```
Adding the execuatble files to 


### Executing program

As stated before, since kEvol is not a single program, there is general structure that must be followed. However, if the prerequistis 
for each stage is qualified, you can continue and start with any stage.

Firts, create a .val file:


Then use the mkconfig program to create the configuration file:
```
mkconfig -f NAME.val
```

Now the configuration file is ready to be used by the main program:
```
kevol -f config.cfg
```

Optionally, you can use the reporter program for perform a novel analyzation:
```
reporter -f report.csv
```

## Help

For any help through using this family, you can use -h or --help command line option to get help about that specific program.
In the case of any ambiguity or software bug or any collaboration, feel free to send me an email at my email address.


## Authors

Contributors names and contact info

NAME: Kiarash Sedghi<br /> 
EMAIL: kiarash.sedghi99@gmail.com




## Version History

* 1.0
    * Initial Release

## License

This project is licensed under the [GNU Affero General Public License v3.0] License - see the LICENSE file for details

