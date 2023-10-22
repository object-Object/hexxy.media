module.exports = {
    apps: [
        {
            name:         "hexxy_media_api",
            script:       "./scripts/pm2/api.sh",
            min_uptime:   "5s",
            max_restarts: 5,
        },
    ]
}
