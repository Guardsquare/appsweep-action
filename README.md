<p align="center">
  <br />
  <br />
  <a href="https://guardsquare.com/appsweep-mobile-application-security-testing">
    <img
      src="https://www.guardsquare.com/hubfs/nav-icon_appsweep-3.png"
      alt="AppSweep" width="30">
    AppSweep
  </a>
</p>

<h4 align="center">GitHub action for AppSweep Mobile Application Security Testing</h4>

## Usage

This action can be used to automate scanning your Android application using a GitHub action.

**Make sure to build the app before calling the step!**

To authenticate, the preferred way is to use ssh agent authentication: You need to add a Service account public key to your team. The private key then needs to be added to your Github Secrets (e.g with the name `SSH_PRIVATE_KEY`). To load the ssh key, you can e.g., use https://github.com/webfactory/ssh-agent. The Appsweep action will then automatically use this key to authenticate the scan.

### Example workflow

```yaml
# This workflow will build the app, and initiate a Guardsquare AppSweep scan of your APK
name: AppSweep mobile application security testing
on: [push]
jobs:
  appsweep-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v2

      # Make sure the @v0.9.0 matches the current version of the action
      - uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Build debug app
        run: ./gradlew assembleDebug

      - name: Upload debug app to AS
        uses: guardsquare/appsweep-action@main
        with:
          input_file: ./app/build/outputs/apk/debug/app-debug.apk
          mapping_file: ./app/build/outputs/mapping/debug/mapping.txt
```

### Inputs

| Input                           | Description                                                                      |
|---------------------------------|----------------------------------------------------------------------------------|
| `INPUT_FILE`                    | The APK that will be uploaded to AppSweep                                        |
| `APPSWEEP_API_KEY`_(optional)_  | Project API key for your AppSweep project, should be stored using Github SECRETS. Only required if you are not using ssh agent authentication |
| `MAPPING_FILE` _(optional)_     | An optional obfuscation mapping file for the build                               |
| `TAGS` _(optional)_             | An optional set of tags to append to your build (format: tag1, tag2)             |
