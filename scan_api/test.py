import acunetix
# print(acunetix.config('https://xuanthulab.net/'))
# acunetix.get_result_id('bfbb3128-7abe-40e5-96f9-cf228f2e213d') => result id = e039d822-6dd5-479b-8a1d-ea26a2cb5643
acunetix.get_list_vuln('bfbb3128-7abe-40e5-96f9-cf228f2e213d', 'e039d822-6dd5-479b-8a1d-ea26a2cb5643')
#                                    scan_id                                result_id