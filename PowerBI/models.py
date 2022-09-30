# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license

class EmbedConfig:

    # Camel casing is used for the member variables as they are going to be serialized and camel case is standard for JSON keys

    tokenId = None
    accessToken = None
    tokenExpiry = None
    reportConfig = None

    def __init__(self, token_id, access_token, token_expiry, report_config):
        self.tokenId = token_id
        self.accessToken = access_token
        self.tokenExpiry = token_expiry
        self.reportConfig = report_config

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license

class EmbedToken:

    # Camel casing is used for the member variables as they are going to be serialized and camel case is standard for JSON keys

    tokenId = None
    token = None
    tokenExpiry = None

    def __init__(self, token_id, token, token_expiry):
        self.tokenId = token_id
        self.token = token
        self.tokenExpiry = token_expiry

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license

class EmbedTokenRequestBody:

    # Camel casing is used for the member variables as they are going to be serialized and camel case is standard for JSON keys

    datasets = None
    reports = None
    targetWorkspaces = None

    def __init__(self):
        self.datasets = []
        self.reports = []
        self.targetWorkspaces = []

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license

class ReportConfig:

    # Camel casing is used for the member variables as they are going to be serialized and camel case is standard for JSON keys

    reportId = None
    reportName = None
    embedUrl = None
    datasetId = None

    def __init__(self, report_id, report_name, embed_url, dataset_id = None):
        self.reportId = report_id
        self.reportName = report_name
        self.embedUrl = embed_url
        self.datasetId = dataset_id