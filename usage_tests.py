from report import Report

def create_bandwidth_report_broken_by_visitor(dmanalyst):
  dmanalyst.create_report(
    ["BANDWIDTH_USED_VOD_BYTES","BANDWIDTH_USED_LIVE_BYTES"],
    ["DAY", "VISITOR_COUNTRY", "VISITOR_DOMAIN_GROUP", "VISITOR_SUBDOMAIN", "VISITOR_DEVICE_TYPE"],
    "2025-05-01",
    "2025-06-16",
    "ALL",
    {}
  )
  dmanalyst.get_download_links_when_ready()

def create_bandwidth_report_broken_by_rendition(dmanalyst):
  dmanalyst.create_report(
    ["BANDWIDTH_USED_VOD_BYTES","BANDWIDTH_USED_LIVE_BYTES"],
    ["DAY", "VIDEO_ID", "VIDEO_TITLE","RENDITION_RESOLUTION","RENDITION_FPS"],
    "2025-05-01",
    "2025-06-16",
    "ALL",
    {}
  )
  dmanalyst.get_download_links_when_ready()

def create_encoding_report_broken_by_rendition(dmanalyst):
  dmanalyst.create_report(
    ["TRANSCODING_USED_VOD_SECONDS","TRANSCODING_USED_LIVE_SECONDS"],
    ["DAY", "VIDEO_ID", "VIDEO_TITLE","RENDITION_RESOLUTION","RENDITION_FPS"],
    "2025-05-01",
    "2025-06-16",
    "ALL",
    {}
  )
  dmanalyst.get_download_links_when_ready()

def create_storage_report_broken_by_video(dmanalyst):
  dmanalyst.create_report(
    ["STORAGE_USED_BYTES"],
    ["DAY", "VIDEO_ID", "VIDEO_TITLE"],
    "2025-06-15",
    "2025-06-16",
    "ALL",
    {}
  )
  dmanalyst.get_download_links_when_ready()

def create_storage_report_broken_by_rendition(dmanalyst):
  dmanalyst.create_report(
    ["STORAGE_USED_BYTES"],
    ["DAY", "VIDEO_ID", "VIDEO_TITLE","RENDITION_RESOLUTION","RENDITION_FPS"],
    "2025-06-15",
    "2025-06-16",
    "ALL",
    {}
  )
  dmanalyst.get_download_links_when_ready()

def run():
  dmanalyst = Report()

  print ("==========BANDWIDTH REPORT BY VISITOR========")
  create_bandwidth_report_broken_by_visitor(dmanalyst)

  print ("==========BANDWIDTH REPORT BY VIDEO RENDITION========")
  create_bandwidth_report_broken_by_rendition(dmanalyst)

  print ("==========ENCODING REPORT BY VIDEO RENDITION========")
  create_encoding_report_broken_by_rendition(dmanalyst)

  print ("==========STORAGE REPORT BY VIDEO ========")
  create_storage_report_broken_by_video(dmanalyst)

  print ("==========STORAGE REPORT BY VIDEO RENDITION ========")
  create_storage_report_broken_by_rendition(dmanalyst)