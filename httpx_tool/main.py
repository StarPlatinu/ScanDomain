from httpx_tool import ToolHTTPX

if __name__ == "__main__":
    array = ['email.bugcrowd.com', 'bugcrowd.com', 'stargate.a.bugcrowd.com', 'ww1.bugcrowd.com', 'portal.bugcrowd.com',
             'sandbox-crowdcontrol.a.bugcrowd.com', 'go.bugcrowd.com', 'levelup.bugcrowd.com', 'api.bugcrowd.com',
             'email.crowdcontrol.bugcrowd.com', 'www.portal.bugcrowd.com', 'www.bugcrowd.com', 'hooks.bugcrowd.com',
             'events.bugcrowd.com', 'collateral.bugcrowd.com', 'gslink.bugcrowd.com', 'itmoah.bugcrowd.com',
             'researcherdocs.bugcrowd.com', 'p.bugcrowd.com', 'ww2.bugcrowd.com', 'email.assetinventory.bugcrowd.com',
             'bounce.bugcrowd.com', 'email.bugs.bugcrowd.com', 'www.submissions.bugcrowd.com', 'hooks.a.bugcrowd.com',
             'crowdcontrol.bugcrowd.com', 'tracker.bugcrowd.com', 'mailgun.bugcrowd.com', 'email.submit.bugcrowd.com',
             'a.bugcrowd.com', 'docs.bugcrowd.com', 'forum.bugcrowd.com', 'forum-new.bugcrowd.com',
             'email.forum.bugcrowd.com', 'www.pages.bugcrowd.com', 'blog.bugcrowd.com',
             'production-sandbox.a.bugcrowd.com', 'files.bugcrowd.com', 'login.bugcrowd.com',
             'submissions.bugcrowd.com', 'documentation.bugcrowd.com', 'assetinventory.bugcrowd.com',
             'pages.bugcrowd.com']
    tool = ToolHTTPX(array)
    tool.enumerate_subdomains()
    # unique_subdomains = tool.get_unique_subdomains()
    # print(f"Unique subdomains found: {unique_subdomains}")



