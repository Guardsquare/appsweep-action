<p align="center">
  <br />
  <br />
  <a href="https://guardsquare.com/appsweep-mobile-application-security-testing">
    <img
      src="https://appsweep.guardsquare.com/AppSweep-blue.svg"
      alt="AppSweep" width="400">
  </a>
</p>


<h4 align="center">GitHub action for AppSweep Mobile Application Security Testing</h4>

## Usage

This action can be used to automate scanning your Android application using a GitHub action

### Example workflow

```yaml
# This workflow will initiate a Guardsquare AppSweep scan of your APK
name: AppSweep mobile application security testing
on: [push]
jobs:
  appsweep-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
        with:
          repository: ''

      - uses: guardsquare/appsweep-action@main
        env:
          APPSWEEP_API_KEY: ${{ secrets.APPSWEEP_API_KEY }}
          INPUT_FILE: InsecureBankv2.apk
          COMMIT_HASH: ${{ steps.vars.outputs.sha_short }}
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `APPSWEEP_API_KEY`  | Project API key for your AppSweep project, should be stored using Github SECRETS    |
| `INPUT_FILE`  | The APK that will be uploaded to AppSweep    |
| `MAPPING_FILE` _(optional)_  | An optional obfuscation mapping file for the build    |
| `LIBRARY_FILE` _(optional)_  | An optional library mapping file for the build    |
| `COMMIT_HASH` _(recommended)_  | An recommended parameter to track the commit hash of the build    |
| `TAGS` _(optional)_  | An optional set of tags to append to your build   |


## Examples

### Using all the optional inputs

This is how to use the optional input.

```yaml
# This workflow will initiate a Guardsquare AppSweep scan of your APK
name: AppSweep mobile application security testing
on: [push]
jobs:
  appsweep-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
        with:
          repository: ''

      - uses: guardsquare/appsweep-action@main
        env:
          APPSWEEP_API_KEY: ${{ secrets.APPSWEEP_API_KEY }}
          INPUT_FILE: InsecureBankv2.apk
          MAPPING_FILE: mapping.txt
          LIBRARY_FILE:
          COMMIT_HASH: ${{ steps.vars.outputs.sha_short }}
          TAGS: release

```
