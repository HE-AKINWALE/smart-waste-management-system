ROLE_PERMISSIONS = {

    "Admin": [

        "manage_users",
        "manage_bins",
        "manage_schedule",
        "manage_records",
        "manage_notifications",
        "view_reports",
        "system_config"

    ],

    "Waste Officer": [

        "manage_bins",
        "manage_schedule",
        "manage_records"

    ],

    "Supervisor": [

        "view_reports",
        "view_dashboard"

    ],

    "Viewer": [

        "view_dashboard"

    ]
}


def get_permissions(role: str):

    return ROLE_PERMISSIONS.get(role, [])