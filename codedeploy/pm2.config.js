module.exports = {
    apps: [
        {
            name:   "HexxyAPI",
            cwd:    "/var/lib/codedeploy_apps/hexxy.media",
            script: "source venv/bin/activate && python -m hexxy_media.api.app",
        },
    ]
}
