# Overview

diaspora\* social network server. See more about diaspora* here - http://diasporafoundation.org

# Usage

To install diaspora*, you will need to know the hostname that will be used. Think carefully before installing, as this cannot be changed after installation.

To set the hostname, you will need to create a configuration file. At minimum it needs the host name setting, but you can configure other parts of the charm at the same time.

To deploy (from the Juju Charm store, once this lands there):

    juju deploy --config=<path to config> diaspora 
  
Until the charm is found in the charm store, deploy from a local repository. To do this first create a path `charms/trusty` somewhere. Change to that path and clone this repository. Create the config file and then:

    juju deploy --config=<path to config> --repository=<path to charms/> local:diaspora

If you don't already have one, you also need to deploy a database:

    juju deploy postgresql

Currently Apache and Redis are installed inside the diaspora* container though this will likely change.

Once services are deployed, create a relation with the database:

    juju add-relation postgresql:db diaspora:db

After everything is installed, you can expose:

    juju expose diaspora

Note down the public address of the diaspora* service and check that it works.

    juju status

## Configuration

### hostname

Pod hostname in the format `domain.tld`. Subdomains are allowed. This is required and *cannot* be changed after installation.

Note! Subfolders are not supported by diaspora* at this moment.

### repository

Default: diaspora/diaspora

Set this to a custom diaspora* repository you would like to use.

### branch

Default: master

### podname

Default: diaspora*

Set a name for your pod.

### ssl_key

Optional. Set your SSL key here as a base64 encoded string.

### ssl_cert

Optional. Set your SSL cert here as a base64 encoded string.

### ssl_snakebite

Default: True

If you don't set `ssl_key` and `ssl_cert`, by default the default snakebite self-signed certifications will be used until a proper cert is set. Set this to false once you transfer the cert manually to the server.

Note! diaspora\* requires a valid SSL certificate for federation. Running a production real diaspora* pod using snakebite certs is **not** possible.

## Upgrading diaspora*

To upgrade the diaspora* instance, you can use the following command:

    juju run --service=diaspora hooks/upgrade-diaspora

## Known Limitations and Issues

Currently this charm supports only the PostgreSQL and Apache combination.

This charm is currently for Ubuntu 14.04 (Trusty) only.

Running several units at the same time has not been tested by the charm author.

# Contact Information

This charm is not officially supported by the [diaspora* project](http://diasporafoundation.org).

Discuss this charm in our Loomio [diaspora* packaging](https://www.loomio.org/d/e7bKczxZ/install-diaspora-easily-with-a-juju-charm-or-ppa) group.

## Charm Contact

Contact the charm author;

* diaspora*: https://iliketoast.net/u/jaywink or jaywink@iliketoast.net
* email: mail@jasonrobinson.me

Please file bugs on [GitHub](https://github.com/jaywink/diaspora-juju). Pull requests also welcome!

# License

[GNU General Public License v3 (GPL-3)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29).

The author provides this charm as is and under no situation is responsible for what it does or doesn't do.