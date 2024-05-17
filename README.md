# 🔍 Handy Voting (for user study)

This project is used for deploying a simple server for a quick user study.




## Introduction

This website has two pages, one being the `index` page, and the other the `admin` page.

### Index Page

![index.page](assets/user.jpg)

The index page is for comparing and voting for results.

The number of Baseline models to be shown can be set as `NUM_MODELS` in `server/config.py`.

In each turn, the set of images shown to the user are from:

* ALL Groundtruth models.
* ALL Target models.
* `NUM_MODELS` Baseline models randomly chosen from all Baseline models.

Only Target (your model) and Baseline models are available for voting.
The order shuffles in each trail.

### Admin Page

![admin.page](assets/admin.jpg)

In the admin page, you can find statistics on the votes for different models.
Currently all properties of the `Model` are shown on this page.

Image generating models are modeled as `Model` ORM objects in this project.

Each `Model` has these properties:

* Id.
* Name. Used in looking for the images.
* Type. Can be `Groundtruth`, `Target`, or `Baseline`.
* Vote Count. The count of votes this model has received.
* Shown Count. That's how many times the model is shown to the user.




## Installation

```
git clone git@github.com:zengyh1900/handy_voting.git
cd handy_voting
pip install -r requirements.txt
```

## Quick start

### Prepare the results for user study

1. Link all the results used for user study to the static folder,
```bash
ln -s /path/to/the/results/of/modelA server/data/modelA
```

2. Setup your configuration in `config.yaml`.

3. Create the database for user study,
```bash
python create_models.py
```

3. RUN.
```bash
export FLASK_APP=server
export FLASK_ENV=production
flask run --host=0.0.0.0
```

You can now access the index page at `http://localhost:5000`
and the admin page at `http://localhost:5000/admin`.

And, your directory hierarchy should look like:

```
.
├── README.md
├── create_models.py
├── **imgvoter.db**
├── requirements.txt
├── server
│   ├── __init__.py
│   ├── config.py
│   ├── models
│   │   └── ...
│   ├── static
│   │   ├── Semantic-UI-CSS
│   │   ├── css
│   │   ├── data
│   │   │   ├── MODEL1
│   │   │   ├── MODEL2
│   │   │   └── ...
│   │   └── img
│   ├── templates
│   │   └── ...
│   └── views.py
└── t...
```


## Credit
original from [@leasunhy](https://github.com/leasunhy)
