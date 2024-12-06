# webserpent
Python Selenium Testing Library

## Logging
Default system logger is set when the environment variable `ENV` is set to dev or not set.
logs to conosle.

## Configurations
To set configs use `webserpent.toml` in the project root folder.
defaults used if not set

### Config Options
#### webdriver
- `headless` bool 
#### webdriver.timeouts
- `implicit` int
- `page_load` int
- `find_element` int
- `element_interaction` int

#### Config Defaults
```
[webdriver]
headless=true

[webdriver.timeouts]
# implicit=None
page_load=10
find_element=5
element_interaction=2
```