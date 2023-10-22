module.exports = {
    apps: [
        {
            name:   "HexxyAPI",
            script: "source venv/bin/activate && python -m hexxy_media.api.app",
        },
    ]
}
