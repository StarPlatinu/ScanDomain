#### Acunetix API Reference

The following API calls can be made using the Acunetix API, as provided in the [Acunetix Jenkins Plugin](https://github.com/jenkinsci/acunetix-plugin/blob/master/src/main/java/com/acunetix/Engine.java).

**1. Add task**

- Method: `POST`
- Endpoint: `/api/v1/targets`
- Headers: `{"X-Auth": apikey, "content-type": "application/json"}`
- Data:
  ```json
  {
    "address": url,
    "description": url,
    "criticality": "10"
  }
  ```

**2. Scan task**

- Method: `POST`
- Endpoint: `/api/v1/scans`
- Headers: `{"X-Auth": apikey, "content-type": "application/json"}`
- Data:
  ```json
  {
    "target_id": target_id,
    "profile_id": "11111111-1111-1111-1111-111111111111",
    "schedule": {
      "disable": false,
      "start_date": null,
      "time_sensitive": false
    }
  }
  ```
  - `target_id`: The result returned by adding the task in the first step.

**3. Get task summary**

- Method: `GET`
- Endpoint: `/api/v1/scans`
- Headers: `{"X-Auth": apikey, "content-type": "application/json"}`

**4. Get task details**

- Method: `GET`
- Endpoint: `/api/v1/scans/+scan_id`
- Headers: `{"X-Auth": apikey, "content-type": "application/json"}`
  - `scan_id`: The ID of the scan task.

**5. Generate report**

- Method: `POST`
- Endpoint: `/api/v1/reports`
- Headers: `{"X-Auth": apikey, "content-type": "application/json"}`
- Data:
  ```json
  {
    "template_id": "11111111-1111-1111-1111-111111111111",
    "source": {
      "list_type": "scans",
      "id_list": [scan_id]
    }
  }
  ```
  - `scan_id`: The ID of the scan task.

**6. Stop scanning**

- Method: `POST`
- Endpoint: `/scans/" + scanId + "/abort`
- Headers: `{"X-Auth": apikey, "content-type": "application/json"}`
  - `scanId`: The ID of the scan to stop.

**7. Delete scan**

- Method: `DELETE`
- Endpoint: `/api/v1/scans/+scan_id`
- Headers: `{"X-Auth": apikey, "content-type": "application/json"}`
  - `scan_id`: The ID of the scan to delete.

For more details, you can refer to the Acunetix API Documentation

---