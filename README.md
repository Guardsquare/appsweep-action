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
# This workflow will build the app, and initiate a Guardsquare AppSweep scan of your APK
name: AppSweep mobile application security testing
on: [push]
jobs:
  upload-app-to-appsweep:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v2

      - name: Build debug app
        run: ./gradlew assembleDebug

      - name: Upload debug app to AS
        uses: guardsquare/appsweep-action@main
        with:
            appsweep_api_key: ${{ secrets.APPSWEEP_API_KEY }}
            input_file: ./app/build/outputs/apk/debug/app-debug.apk
            mapping_file: ./app/build/outputs/mapping/debug/mapping.txt
```

### Inputs

| Input                         | Description                                                                      |
|-------------------------------|----------------------------------------------------------------------------------|
| `APPSWEEP_API_KEY`            | Project API key for your AppSweep project, should be stored using Github SECRETS |
| `INPUT_FILE`                  | The APK that will be uploaded to AppSweep                                        |
| `MAPPING_FILE` _(optional)_   | An optional obfuscation mapping file for the build                               |
| `TAGS` _(optional)_           | An optional set of tags to append to your build (format: tag1, tag2)             |
