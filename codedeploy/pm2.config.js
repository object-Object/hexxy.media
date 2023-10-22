module.exports = {
    apps: [
        {
            name:         "HexxyAPI",
            script:       "./scripts/pm2/HexxyAPI.sh",
            min_uptime:   5,
            max_restarts: 5,
        },
    ]
}
