# Postfolio Manager

## Getting started

### Prerequisite Software

| **No** | **Name**           | **Version** | **Notes**                                                                        |
| ------ | ------------------ | ----------- | -------------------------------------------------------------------------------- |
| 1      | Jupyter               | **Latest**          |
| 2    | Docker             | **Latest**  |

### Start application locally

```docker
docker-compose up
```

## Secrets File
  - The config file is `config/app_secrets/common_settings.yml`. I would generally gitignore it, and not push it to the repo, but doing it here for the time being.
  - You can change the database from the secrets file
  - The database is exposed on port `5440` and the application is exposed on port `3012`

## API Docs
  - API documentation can be accessed [here](http://localhost:3012/api-docs) when docker-compose is running. APIs can be tried out there directly from the browser.

## Example Usage
  - Assignment can be found [here](./assignment.pdf)
  - An example implementation can be found by opening the jupyter notebook [here](./assignment_example.ipynb). The notebook could also be run when docker-compose is running.

## Miscellaneus Info
  - Using django as backend framework.
  - core logic can be found in the `stashaway` django app.
  - project is using swagger for API docs generation.
## Style Guides

- [PEP8](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
