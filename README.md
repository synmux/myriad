# is there support in the paypal api for listing and cancelling Pre-approved payments?

## Support for Listing and Cancelling Pre-Approved Payments in PayPal API

Yes, **the PayPal API does provide support for both listing and cancelling pre-approved payments**, though it's important to note that the endpoints handling this functionality are now **deprecated**.[1]

### REST API (Billing Agreements v1 - Deprecated)

The current REST API provides two key endpoints for managing pre-approved payments:[1]

**List Billing Agreements**[1]

- **Endpoint**: `GET /v1/payments/billing-agreements`
- **Purpose**: Retrieves all billing agreements associated with a merchant account
- **Response**: Returns HTTP 200 OK with a JSON list of all agreements

**Cancel Billing Agreement**[1]

- **Endpoint**: `POST /v1/payments/billing-agreements/{agreement_id}/cancel`
- **Purpose**: Cancels a specific billing agreement by its ID
- **Request Body**: Accepts an optional `agreement_state_descriptor` object with a note explaining the cancellation reason
- **Response**: Returns HTTP 204 No Content on success

### Additional Management Endpoints

Beyond cancellation and listing, the Billing Agreements API also supports:[1]

- **Suspend**: `POST /v1/payments/billing-agreements/{agreement_id}/suspend` — temporarily pauses an agreement
- **Reactivate**: `POST /v1/payments/billing-agreements/{agreement_id}/re_activate` — re-enables a suspended agreement
- **Get Details**: `GET /v1/payments/billing-agreements/{agreement_id}` — retrieves full agreement information
- **Update**: `PATCH /v1/payments/billing-agreements/{agreement_id}` — modifies agreement details
- **List Transactions**: `GET /v1/payments/billing-agreements/{agreement_id}/transactions` — retrieves transaction history for an agreement

### Legacy NVP/SOAP API Support

For older integrations, PayPal's NVP/SOAP API also provides functionality through:[2]

- `ManageRecurringPaymentsProfileStatus` — for suspending, reactivating, or cancelling recurring payment profiles
- Profile ID retrieval methods for identifying agreements to manage

### Recommended Path Forward

**Important**: PayPal strongly recommends migrating to the newer `/v1/billing/subscriptions` endpoints rather than the deprecated `/v1/payments/billing-agreements` endpoints. The subscriptions API provides more modern functionality and better supports current PayPal payment patterns, including support for variable amounts and more flexible billing arrangements through the Subscriptions or recurring billing modules.[1]

## Citations (Part 1)

[1] [Billing Agreements](https://developer.paypal.com/docs/api/payments.billing-agreements/v1/)
[2] [Cancelling Subscriptions Created with PayPal Standard via ...](https://thereforei.am/2012/07/03/cancelling-subscriptions-created-with-paypal-standard-via-the-express-checkout-api/)
[3] [How To Cancel Pre Approved Payments In Paypal](https://www.youtube.com/watch?v=IL7nO1LNJpU)
[4] [Payflow Recurring Billing Service User's Guide](https://developer.paypal.com/api/nvp-soap/payflow/recurring-billing/)
[5] [PayPal for API only - Docs](https://www.checkout.com/docs/payments/add-payment-methods/paypal/api-only)
[6] [How To Cancel PreApproved Paypal Payments 2023](https://www.youtube.com/watch?v=KDm9D1jWEgE)
[7] [Recurring payments](https://developer.paypal.com/braintree/docs/guides/paypal/recurring-payments/javascript/v3/)
[8] [paypal Preapproval API - php](https://stackoverflow.com/questions/32717946/paypal-preapproval-api)
[9] [How to Cancel PayPal Billing Agreement or Automatic ...](https://www.shoutmeloud.com/paypal-how-to-cancel-automatic-renewal-of-subscriptions.html)
[10] [Recurring payments module](https://developer.paypal.com/studio/checkout/standard/customize/recurring-payments-module)
[11] [ExprEss ChECkout](https://www.paypalobjects.com/WEBSCR-640-20131020-1/en_US/Marketing/pdf/ec_quickstartguide.pdf)
[12] [Automatic Payment | Update Recurring Payments](https://www.paypal.com/us/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[13] [DoReferenceTransaction API Operation (NVP)](https://developer.paypal.com/api/nvp-soap/do-reference-transaction-nvp/)
[14] [How can I cancel a PayPal Billing Agreement via an API call](https://stackoverflow.com/questions/20577412/how-can-i-cancel-a-paypal-billing-agreement-via-an-api-call)
[15] [SetCustomerBillingAgreement API Operation (NVP)](https://developer.paypal.com/api/nvp-soap/set-customer-billing-agreement-nvp/)
[16] [How do you cancel a PayPal subscription through their api?](https://stackoverflow.com/questions/4348579/how-do-you-cancel-a-paypal-subscription-through-their-api)
[17] [Upgrade your checkout integration](https://developer.paypal.com/upgrade/ec/guide/Billing%20Agreement%20Without%20Purchase/)
[18] [DoExpressCheckoutPayment API Operation (NVP)](https://developer.paypal.com/api/nvp-soap/do-express-checkout-payment-nvp/)
[19] [Cancelling paypal subscriptions using their API - how to keep the account active for the already paid peroid?](https://stackoverflow.com/questions/63631957/cancelling-paypal-subscriptions-using-their-api-how-to-keep-the-account-active)
[20] [Detecting cancellation of a paypal billing agreement setup ...](https://stackoverflow.com/questions/13622957/detecting-cancellation-of-a-paypal-billing-agreement-setup-with-reference-transa)

---

## Write me a Python script which I can edit to add my API keys and credentials which will list all my pre approved payments and cancel them. Give it two modes: "old" using the deprecated APIs and "new" using the new ones

Below is an editable Python script that supports two modes: **old** (deprecated Billing Agreements v1) and **new** (Subscriptions v1). The old mode uses `GET /v1/payments/billing-agreements` and `POST /v1/payments/billing-agreements/{id}/cancel` as documented in the deprecated Billing Agreements API. The new mode uses the Subscriptions API (v1) and calls the “list all subscriptions for merchant account” and cancel endpoints.\[1\]\[2\]

## Python script

```python
#!/usr/bin/env python3
"""
paypal_cancel_preapproved.py

Two modes:
  - old: deprecated Billing Agreements v1 (/v1/payments/billing-agreements)
  - new: current Subscriptions v1 (/v1/billing/subscriptions)

Usage examples:
  python paypal_cancel_preapproved.py --mode old --env live --list
  python paypal_cancel_preapproved.py --mode old --env live --cancel-all --reason "User requested"
  python paypal_cancel_preapproved.py --mode new --env live --list
  python paypal_cancel_preapproved.py --mode new --env live --cancel-all --reason "User requested"

Notes:
- This script uses OAuth2 client_credentials to get an access token. [web:22][web:21]
- Base URLs:
    Sandbox: https://api-m.sandbox.paypal.com
    Live:    https://api-m.paypal.com [web:26]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import requests


# -----------------------------
# CONFIG: Fill these in
# -----------------------------
PAYPAL_CLIENT_ID = "PUT_YOUR_CLIENT_ID_HERE"
PAYPAL_CLIENT_SECRET = "PUT_YOUR_CLIENT_SECRET_HERE"


# -----------------------------
# REST helpers
# -----------------------------
def base_url(env: str) -> str:
    if env == "sandbox":
        return "https://api-m.sandbox.paypal.com"
    if env == "live":
        return "https://api-m.paypal.com"
    raise ValueError("env must be 'sandbox' or 'live'")


def get_access_token(env: str, client_id: str, client_secret: str) -> str:
    """
    OAuth2 token endpoint:
      POST https://api-m.{env}.paypal.com/v1/oauth2/token
    grant_type=client_credentials [web:21][web:22]
    """
    url = f"{base_url(env)}/v1/oauth2/token"
    max_retries = 3
    last_details = None

    for attempt in range(max_retries):
        try:
            r = requests.post(
                url,
                headers={"Accept": "application/json"},
                auth=(client_id, client_secret),
                data={"grant_type": "client_credentials"},
                timeout=30,
            )
            if r.status_code == 200:
                return r.json()["access_token"]

            last_details = f"Status: {r.status_code}, Body: {r.text}"

            # Retry on server errors (5xx)
            if 500 <= r.status_code < 600:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                continue

            # Non-retriable error (e.g. 4xx)
            raise RuntimeError(f"Token request failed: {r.status_code} {r.text}")

        except requests.RequestException as e:
            last_details = f"Exception: {e}"
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            continue

    raise RuntimeError(f"Token request failed after {max_retries} attempts. Last details: {last_details}")


def api_request(
    env: str,
    method: str,
    path: str,
    token: str,
    json_body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> requests.Response:
    url = f"{base_url(env)}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    r = requests.request(
        method=method,
        url=url,
        headers=headers,
        json=json_body,
        params=params,
        timeout=60,
    )
    return r


# -----------------------------
# OLD MODE: Billing Agreements v1 (DEPRECATED)
# -----------------------------
def old_list_billing_agreements(env: str, token: str) -> List[Dict[str, Any]]:
    """
    GET /v1/payments/billing-agreements [web:11]
    """
    r = api_request(env, "GET", "/v1/payments/billing-agreements", token)
    if r.status_code != 200:
        raise RuntimeError(f"List billing agreements failed: {r.status_code} {r.text}")

    data = r.json()
    # The API returns an object; agreements usually appear under 'agreements' (but keep defensive). [web:11]
    if isinstance(data, dict):
        return data.get("agreements") or data.get("billing_agreements") or data.get("items") or []
    if isinstance(data, list):
        return data
    return []


def old_cancel_billing_agreement(env: str, token: str, agreement_id: str, reason: str) -> None:
    """
    POST /v1/payments/billing-agreements/{agreement_id}/cancel [web:11]
    Body supports an 'agreement_state_descriptor' with a note. [web:11]
    """
    body = {"agreement_state_descriptor": {"note": reason}}
    r = api_request(env, "POST", f"/v1/payments/billing-agreements/{agreement_id}/cancel", token, json_body=body)
    if r.status_code != 204:
        raise RuntimeError(f"Cancel billing agreement {agreement_id} failed: {r.status_code} {r.text}")


# -----------------------------
# NEW MODE: Subscriptions v1
# -----------------------------
def new_list_subscriptions(env: str, token: str, page_size: int = 20, max_pages: int = 200) -> List[Dict[str, Any]]:
    """
    Lists all subscriptions for merchant account (Subscriptions v1). [web:40]
    Uses pagination (page, page_size) to retrieve multiple pages where supported. [web:40]
    """
    results: List[Dict[str, Any]] = []
    page = 1

    while page <= max_pages:
        params = {"page_size": page_size, "page": page}
        r = api_request(env, "GET", "/v1/billing/subscriptions", token, params=params)
        if r.status_code != 200:
            # Some accounts / regions may not support listing; PayPal varies by capability.
            raise RuntimeError(f"List subscriptions failed: {r.status_code} {r.text}")

        payload = r.json()
        items = payload.get("subscriptions") or payload.get("items") or []
        if not items:
            break
        results.extend(items)

        # If API provides total_pages, use it; otherwise just keep paging until empty. [web:40]
        total_pages = payload.get("total_pages")
        if total_pages is not None and page >= int(total_pages):
            break

        page += 1

    return results


def new_cancel_subscription(env: str, token: str, subscription_id: str, reason: str) -> None:
    """
    POST /v1/billing/subscriptions/{subscription_id}/cancel [web:40]
    """
    body = {"reason": reason}
    r = api_request(env, "POST", f"/v1/billing/subscriptions/{subscription_id}/cancel", token, json_body=body)
    # Common successful responses are 204 No Content for cancel; treat 200/204 as ok. [web:40]
    if r.status_code not in (200, 204):
        raise RuntimeError(f"Cancel subscription {subscription_id} failed: {r.status_code} {r.text}")


# -----------------------------
# CLI / main
# -----------------------------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["old", "new"], required=True, help="old=Billing Agreements v1 (deprecated), new=Subscriptions v1")
    p.add_argument("--env", choices=["sandbox", "live"], default="sandbox", help="PayPal environment")
    p.add_argument("--list", action="store_true", help="List agreements/subscriptions")
    p.add_argument("--cancel-all", action="store_true", help="Cancel everything returned by list")
    p.add_argument("--reason", default="Cancelled via API/script", help="Cancellation reason/note")
    p.add_argument("--dry-run", action="store_true", help="Show what would be cancelled but do not cancel")
    p.add_argument("--page-size", type=int, default=20, help="New mode: page size for subscription listing")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if PAYPAL_CLIENT_ID.startswith("PUT_") or PAYPAL_CLIENT_SECRET.startswith("PUT_"):
        print("ERROR: Edit PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET in the script first.", file=sys.stderr)
        return 2

    token = get_access_token(args.env, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)

    if args.mode == "old":
        items = old_list_billing_agreements(args.env, token)
        # Agreements objects include 'id' and 'state' in the Billing Agreements API. [web:11]
        if args.list:
            print(json.dumps(items, indent=2, sort_keys=True))
        if args.cancel_all:
            for a in items:
                agreement_id = a.get("id")
                state = a.get("state")
                if not agreement_id:
                    continue
                print(f"[old] cancel {agreement_id} (state={state})")
                if not args.dry_run:
                    old_cancel_billing_agreement(args.env, token, agreement_id, args.reason)
        return 0

    if args.mode == "new":
        items = new_list_subscriptions(args.env, token, page_size=args.page_size)
        # Subscription objects typically include 'id' and 'status'. [web:40]
        if args.list:
            print(json.dumps(items, indent=2, sort_keys=True))
        if args.cancel_all:
            for s in items:
                subscription_id = s.get("id")
                status = s.get("status")
                if not subscription_id:
                    continue
                print(f"[new] cancel {subscription_id} (status={status})")
                if not args.dry_run:
                    new_cancel_subscription(args.env, token, subscription_id, args.reason)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## Notes before running

- The “old” Billing Agreements endpoints are explicitly marked deprecated by PayPal, and PayPal directs new integrations to use `/v1/billing/subscriptions` instead.[1]
- The script uses PayPal’s REST OAuth2 token flow via `POST /v1/oauth2/token` with `grant_type=client_credentials` and the `api-m` base URLs for sandbox/live.\[3\]\[4\]

Do the “pre-approved payments” you want to cancel correspond to “Billing Agreements” (reference transactions) or “Subscriptions” (fixed billing cycles)?

## Citations (Part 2)

[1] [Billing Agreements](https://developer.paypal.com/docs/api/payments.billing-agreements/v1/)
[2] [Subscriptions - PayPal Developer](https://developer.paypal.com/docs/api/subscriptions/v1/)
[3] [How do I get an Access Token? | PayPal US](https://www.paypal.com/us/cshelp/article/how-do-i-get-an-access-token-ts2128)
[4] [Making PayPal REST API requests](https://docs.paypal.ai/developer/how-to/api/make-api-requests)
[5] [Authentication](https://developer.paypal.com/api/rest/authentication/)
[6] [How do I send a fetch request to Paypal's Oath API (v2)?](https://stackoverflow.com/questions/74779027/how-do-i-send-a-fetch-request-to-paypals-oath-api-v2)
[7] [PayPal Access/Bearer token](https://stackoverflow.com/questions/69194032/paypal-access-bearer-token)
[8] [Struggle retrieving Paypal Access Token using ClientId ...](https://forum.bubble.io/t/struggle-retrieving-paypal-access-token-using-clientid-and-secret-2021/158580)
[9] [[PayPal] Authentication - OAuth 2.0 Get access token](https://jhlee-developer.tistory.com/entry/PayPal-Authentication-OAuth-20-access-tokens)
[10] [What is the PayPal API base link for Live accounts?](https://stackoverflow.com/questions/76024811/what-is-the-paypal-api-base-link-for-live-accounts)
[11] [PayPal Billing Agreements with PHP in 2023](https://stackoverflow.com/questions/75067717/paypal-billing-agreements-with-php-in-2023)
[12] [OAuth2 client credentials](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow)
[13] [API requests](https://developer.paypal.com/api/rest/requests/)
[14] [Policy Updates](https://www.paypal.com/gb/legalhub/paypal/upcoming-policies-full?locale.x=en_GB)
[15] [OAuth Selection for PayPal - Need help](https://forum.bubble.io/t/oauth-selection-for-paypal/31587)
[16] [PayPal 決済の実装方法](https://qiita.com/PPJP/items/db5c57991c2c3fe80ac7)
[17] [Deprecated Payment Methods (2025) - Documentation](https://support.eventespresso.com/article/612-deprecated-payment-methods-2025)
[18] [PayPal Get Access Token cURL Syntax Converted to ...](https://wordpress.org/support/topic/paypal-get-access-token-curl-syntax-converted-to-wp_remote_post-syntax/)
[19] [PayPal Community](https://www.paypal-community.com/t5/Products-Services/API-transaction-with-API-url-https-api-m-sandbox-paypal-com-v1/td-p/3136899)
[20] [Deprecated resources](https://developer.paypal.com/api/rest/deprecated-resources/)
[21] [Client Credentials](https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/)
[22] [Make paypal subscriptions API request to get subscription info on server - auth wrapper?](https://stackoverflow.com/questions/66142347/make-paypal-subscriptions-api-request-to-get-subscription-info-on-server-auth)
[23] [PayPal Subscriptions: Tailored Billing for Every Customer](https://developer.paypal.com/docs/subscriptions/)
[24] [Get all subscriptions - Paypal Docs](https://docs.paypal.ai/reference/api/rest/subscriptions/get-all-subscriptions)
[25] [Manage subscriptions - Paypal Docs](https://docs.paypal.ai/limited-release/usage-based-billing/manage-entities/manage-subscriptions)
[26] [Cancelling Subscriptions Created with PayPal Standard via ...](https://thereforei.am/2012/07/03/cancelling-subscriptions-created-with-paypal-standard-via-the-express-checkout-api/)
[27] [Subscription Implementation - PayPal Community](https://ppl.lithium.com/t5/REST-APIs/Subscription-Implementation/td-p/3105199)
[28] [paypal-rest-api-specifications/openapi/billing_subscriptions_v1.json at main · paypal/paypal-rest-api-specifications](https://github.com/paypal/paypal-rest-api-specifications/blob/main/openapi/billing_subscriptions_v1.json)
[29] [Cancel Subscription - PayPal Public API Documentation](https://developers.qodex.ai/paypal-public-api/paypal-apis/subscriptions-subscriptions-1/cancel-subscription)
[30] [Billing Plans - developer Paypal](https://developer.paypal.com/docs/api/payments.billing-plans/v1/)
[31] [PayPal Subscriptions: How to get Subscription details after payment?](https://stackoverflow.com/questions/71806237/paypal-subscriptions-how-to-get-subscription-details-after-payment)
[32] [PayPal Community](https://www.paypal-community.com/t5/PayPal-Payments-Standard/Cancel-Subscription-Button/td-p/1832778)
[33] [Create a new subscription - Paypal Docs](https://docs.paypal.ai/reference/api/rest/subscriptions/create-a-new-subscription)
[34] [Solved: Using the Subscriptions API - PayPal Community](https://ppl.lithium.com/t5/REST-APIs/Using-the-Subscriptions-API/td-p/2723216)
[35] [Cancel a subscription - Paypal Docs](https://docs.paypal.ai/reference/api/rest/subscriptions/cancel-a-subscription)
[36] [PayPal Subscriptions API: retrieving information for a existing billing plan ID using curl](https://stackoverflow.com/questions/65366505/paypal-subscriptions-api-retrieving-information-for-a-existing-billing-plan-id)
[37] [PayPal Community](https://www.paypal-community.com/t5/REST-APIs/GET-v1-billing-subscriptions-Why-does-this-endpoint-not-exist/td-p/3132097)
[38] [Manage subscriptions](https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/manage-subscriptions/)
[39] [Is billing agreement deprecated as created billing here? · Issue #419 · paypal/PayPal-NET-SDK](https://github.com/paypal/PayPal-NET-SDK/issues/419)
[40] [PayPal Community](https://www.paypal-community.com/t5/REST-APIs/Using-the-Subscriptions-API/td-p/2723216)

---

## I'm really not sure, so I want the script to be able to handle both

Here’s an updated script that can do **both** in one run: it will (1) list + optionally cancel deprecated **Billing Agreements v1** _and_ (2) list + optionally cancel **Subscriptions v1**, using the documented list/cancel endpoints for each API.[1]

## One script, handles both

```python
#!/usr/bin/env python3
"""
paypal_nuke_preapproved.py

Lists and (optionally) cancels *both* kinds of "pre-approved payments":

  OLD (deprecated):
    - Billing Agreements v1
      GET  /v1/payments/billing-agreements
      POST /v1/payments/billing-agreements/{agreement_id}/cancel
    Deprecation notice: /v1/payments/billing-agreements is deprecated in favor of /v1/billing/subscriptions. [web:1]

  NEW:
    - Subscriptions v1
      GET  /v1/billing/subscriptions        (list all subscriptions for merchant account) [web:0]
      POST /v1/billing/subscriptions/{id}/cancel [web:0]

Usage:
  python paypal_nuke_preapproved.py --env live --list
  python paypal_nuke_preapproved.py --env live --cancel-all --reason "User requested"
  python paypal_nuke_preapproved.py --env live --cancel-all --dry-run

Requirements:
  pip install requests
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple

import requests


# =============================
# CONFIG: edit these
# =============================
PAYPAL_CLIENT_ID = "PUT_YOUR_CLIENT_ID_HERE"
PAYPAL_CLIENT_SECRET = "PUT_YOUR_CLIENT_SECRET_HERE"


# =============================
# Core REST plumbing
# =============================
def base_url(env: str) -> str:
    if env == "sandbox":
        return "https://api-m.sandbox.paypal.com"
    if env == "live":
        return "https://api-m.paypal.com"
    raise ValueError("env must be sandbox|live")


def get_access_token(env: str, client_id: str, client_secret: str) -> str:
    url = f"{base_url(env)}/v1/oauth2/token"
    r = requests.post(
        url,
        auth=(client_id, client_secret),
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Token request failed: {r.status_code} {r.text}")
    return r.json()["access_token"]


def api_request(
    env: str,
    method: str,
    path: str,
    token: str,
    json_body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> requests.Response:
    url = f"{base_url(env)}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    return requests.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=json_body,
        timeout=60,
    )


# =============================
# OLD: Billing Agreements v1 (deprecated)
# =============================
def old_list_billing_agreements(env: str, token: str) -> List[Dict[str, Any]]:
    r = api_request(env, "GET", "/v1/payments/billing-agreements", token)
    if r.status_code != 200:
        raise RuntimeError(f"[old] list failed: {r.status_code} {r.text}")

    payload = r.json()
    # PayPal docs show an object response; field names can vary, be defensive. [web:1]
    if isinstance(payload, dict):
        return payload.get("agreements") or payload.get("billing_agreements") or payload.get("items") or []
    if isinstance(payload, list):
        return payload
    return []


def old_cancel_billing_agreement(env: str, token: str, agreement_id: str, note: str) -> None:
    body = {"agreement_state_descriptor": {"note": note}}
    r = api_request(env, "POST", f"/v1/payments/billing-agreements/{agreement_id}/cancel", token, json_body=body)
    if r.status_code != 204:
        raise RuntimeError(f"[old] cancel {agreement_id} failed: {r.status_code} {r.text}")


# =============================
# NEW: Subscriptions v1
# =============================
def new_list_subscriptions(
    env: str,
    token: str,
    page_size: int = 20,
    max_pages: int = 200,
    statuses: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Lists all subscriptions for a merchant account; supports paging. [web:0]
    """
    out: List[Dict[str, Any]] = []
    page = 1
    while page <= max_pages:
        params: Dict[str, Any] = {"page_size": page_size, "page": page}
        if statuses:
            params["statuses"] = statuses  # docs list 'statuses' as a filter. [web:0]

        r = api_request(env, "GET", "/v1/billing/subscriptions", token, params=params)
        if r.status_code != 200:
            raise RuntimeError(f"[new] list failed: {r.status_code} {r.text}")

        payload = r.json()
        items = payload.get("subscriptions") or payload.get("items") or []
        if not items:
            break

        out.extend(items)

        total_pages = payload.get("total_pages")
        if total_pages is not None and page >= int(total_pages):
            break

        page += 1

    return out


def new_cancel_subscription(env: str, token: str, subscription_id: str, reason: str) -> None:
    body = {"reason": reason}
    r = api_request(env, "POST", f"/v1/billing/subscriptions/{subscription_id}/cancel", token, json_body=body)
    # Docs show 204 No Content on success. [web:0]
    if r.status_code != 204 and r.status_code != 200:
        raise RuntimeError(f"[new] cancel {subscription_id} failed: {r.status_code} {r.text}")


# =============================
# Orchestration
# =============================
def summarize_old(a: Dict[str, Any]) -> Tuple[str, str, str]:
    return (
        a.get("id", ""),
        a.get("state", ""),
        a.get("description", "") or a.get("name", ""),
    )


def summarize_new(s: Dict[str, Any]) -> Tuple[str, str, str]:
    return (
        s.get("id", ""),
        s.get("status", ""),
        s.get("plan_id", "") or s.get("custom_id", "") or "",
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--env", choices=["sandbox", "live"], default="sandbox")
    p.add_argument("--list", action="store_true", help="Print raw JSON lists for both old/new")
    p.add_argument("--cancel-all", action="store_true", help="Cancel everything discovered (old + new)")
    p.add_argument("--dry-run", action="store_true", help="Show what would be cancelled, but do not cancel")
    p.add_argument("--reason", default="Cancelled via script", help="Reason/note passed to cancel endpoints")
    p.add_argument("--page-size", type=int, default=20, help="New mode: page size for subscription listing (max 20) [web:0]")
    p.add_argument("--new-statuses", default=None, help="New mode: optional statuses filter, e.g. ACTIVE,SUSPENDED [web:0]")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if PAYPAL_CLIENT_ID.startswith("PUT_") or PAYPAL_CLIENT_SECRET.startswith("PUT_"):
        print("ERROR: Edit PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET first.", file=sys.stderr)
        return 2

    token = get_access_token(args.env, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)

    # 1) OLD
    old_items: List[Dict[str, Any]] = []
    old_error: Optional[str] = None
    try:
        old_items = old_list_billing_agreements(args.env, token)
    except Exception as e:
        old_error = str(e)

    # 2) NEW
    new_items: List[Dict[str, Any]] = []
    new_error: Optional[str] = None
    try:
        new_items = new_list_subscriptions(
            args.env, token, page_size=args.page_size, statuses=args.new_statuses
        )
    except Exception as e:
        new_error = str(e)

    # Output
    print("== Results ==")
    if old_error:
        print(f"[old] ERROR: {old_error}")
    else:
        print(f"[old] billing agreements found: {len(old_items)}")
        for a in old_items:
            _id, state, desc = summarize_old(a)
            if _id:
                print(f"  [old] {_id}  state={state}  desc={desc}")

    if new_error:
        print(f"[new] ERROR: {new_error}")
    else:
        print(f"[new] subscriptions found: {len(new_items)}")
        for s in new_items:
            _id, status, ref = summarize_new(s)
            if _id:
                print(f"  [new] {_id}  status={status}  ref={ref}")

    if args.list:
        print("\n== Raw JSON ==")
        print(json.dumps({"old": old_items, "new": new_items}, indent=2, sort_keys=True))

    # Cancel
    if args.cancel_all:
        print("\n== Cancel ==")
        if old_error is None:
            for a in old_items:
                agreement_id = a.get("id")
                if not agreement_id:
                    continue
                print(f"[old] cancel {agreement_id}")
                if not args.dry_run:
                    old_cancel_billing_agreement(args.env, token, agreement_id, args.reason)

        if new_error is None:
            for s in new_items:
                subscription_id = s.get("id")
                if not subscription_id:
                    continue
                print(f"[new] cancel {subscription_id}")
                if not args.dry_run:
                    new_cancel_subscription(args.env, token, subscription_id, args.reason)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Important caveats

- PayPal’s **Billing Agreements v1** docs explicitly mark `/v1/payments/billing-agreements` as deprecated and point to `/v1/billing/subscriptions` instead, so “old” may fail depending on account/API permissions.[1]
- The Subscriptions API explicitly documents “List all subscriptions for merchant account” plus `POST .../{id}/cancel` with a JSON `{ "reason": "..." }` and a `204 No Content` success response.

If this is for your _personal_ PayPal account (not a merchant integration), PayPal’s “Automatic payments” UI often shows agreements that are not accessible via these merchant APIs; if you run this and both lists come back empty, share the HTTP status + response body (redacting tokens) and it can be adjusted.

## Citations (Part 3)

## [1] [How To Cancel Pre Approved Payments In Paypal](https://www.youtube.com/watch?v=IL7nO1LNJpU)

## This is a personal account and refers to things I am paying, not money I am collecting. Also, add a flag to dump the raw responses you're talking about

For a **personal** PayPal account (you’re the payer), PayPal’s public developer APIs generally don’t provide a “list all my automatic payments as a buyer” endpoint; the APIs you’ve been looking at are primarily for the **merchant** side (listing billing agreements/subscriptions _for a merchant account_). That means a script using those APIs will often return empty lists or permission errors unless you’re authenticating as the merchant who created the agreement.\[1\]\[2\]\[3\]

## Updated script (adds raw-response dumping)

This version keeps the “try both old and new” behaviour, and adds `--dump-raw` to print the raw HTTP status, headers, and body for each call (token + list + cancel), so you can see exactly what PayPal is returning.

```python
#!/usr/bin/env python3
"""
paypal_nuke_preapproved.py

IMPORTANT CONTEXT:
- The Subscriptions v1 API includes "List all subscriptions for merchant account". [web:40]
- The Billing Agreements v1 endpoints are deprecated and were used for merchant-managed recurring agreements. [web:11]
- For a personal (payer) account, PayPal usually expects you to manage "Automatic Payments" in the UI. [web:10]

This script still attempts to list/cancel both:
  OLD: /v1/payments/billing-agreements (deprecated) [web:11]
  NEW: /v1/billing/subscriptions (merchant list) [web:40]

Flags:
  --dump-raw : dump raw HTTP responses (status/headers/body) for troubleshooting.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple

import requests


# =============================
# CONFIG: edit these
# =============================
PAYPAL_CLIENT_ID = "PUT_YOUR_CLIENT_ID_HERE"
PAYPAL_CLIENT_SECRET = "PUT_YOUR_CLIENT_SECRET_HERE"


# =============================
# Core REST plumbing
# =============================
def base_url(env: str) -> str:
    if env == "sandbox":
        return "https://api-m.sandbox.paypal.com"
    if env == "live":
        return "https://api-m.paypal.com"
    raise ValueError("env must be sandbox|live")


def dump_response(label: str, r: requests.Response) -> None:
    print(f"\n--- {label} ---")
    print(f"{r.request.method} {r.request.url}")
    print(f"Status: {r.status_code}")
    print("Response headers:")
    for k, v in sorted(r.headers.items()):
        print(f"  {k}: {v}")
    # Body (best-effort)
    ct = r.headers.get("content-type", "")
    print("Body:")
    if "application/json" in ct.lower():
        try:
            print(json.dumps(r.json(), indent=2, sort_keys=True))
        except Exception:
            print(r.text)
    else:
        print(r.text)


def get_access_token(env: str, client_id: str, client_secret: str, dump_raw: bool = False) -> str:
    url = f"{base_url(env)}/v1/oauth2/token"
    r = requests.post(
        url,
        auth=(client_id, client_secret),
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
        timeout=30,
    )
    if dump_raw:
        dump_response("oauth2_token", r)
    if r.status_code != 200:
        raise RuntimeError(f"Token request failed: {r.status_code} {r.text}")
    return r.json()["access_token"]


def api_request(
    env: str,
    method: str,
    path: str,
    token: str,
    json_body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> requests.Response:
    url = f"{base_url(env)}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    return requests.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=json_body,
        timeout=60,
    )


# =============================
# OLD: Billing Agreements v1 (deprecated)
# =============================
def old_list_billing_agreements(env: str, token: str, dump_raw: bool = False) -> List[Dict[str, Any]]:
    r = api_request(env, "GET", "/v1/payments/billing-agreements", token)
    if dump_raw:
        dump_response("old_list_billing_agreements", r)
    if r.status_code != 200:
        raise RuntimeError(f"[old] list failed: {r.status_code} {r.text}")

    payload = r.json()
    if isinstance(payload, dict):
        return payload.get("agreements") or payload.get("billing_agreements") or payload.get("items") or []
    if isinstance(payload, list):
        return payload
    return []


def old_cancel_billing_agreement(env: str, token: str, agreement_id: str, note: str, dump_raw: bool = False) -> None:
    body = {"agreement_state_descriptor": {"note": note}}
    r = api_request(env, "POST", f"/v1/payments/billing-agreements/{agreement_id}/cancel", token, json_body=body)
    if dump_raw:
        dump_response(f"old_cancel_billing_agreement:{agreement_id}", r)
    if r.status_code != 204:
        raise RuntimeError(f"[old] cancel {agreement_id} failed: {r.status_code} {r.text}")


# =============================
# NEW: Subscriptions v1
# =============================
def new_list_subscriptions(
    env: str,
    token: str,
    page_size: int = 20,
    max_pages: int = 200,
    statuses: Optional[str] = None,
    dump_raw: bool = False,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    page = 1

    while page <= max_pages:
        params: Dict[str, Any] = {"page_size": page_size, "page": page}
        if statuses:
            params["statuses"] = statuses

        r = api_request(env, "GET", "/v1/billing/subscriptions", token, params=params)
        if dump_raw:
            dump_response(f"new_list_subscriptions:page={page}", r)
        if r.status_code != 200:
            raise RuntimeError(f"[new] list failed: {r.status_code} {r.text}")

        payload = r.json()
        items = payload.get("subscriptions") or payload.get("items") or []
        if not items:
            break

        out.extend(items)

        total_pages = payload.get("total_pages")
        if total_pages is not None and page >= int(total_pages):
            break

        page += 1

    return out


def new_cancel_subscription(env: str, token: str, subscription_id: str, reason: str, dump_raw: bool = False) -> None:
    body = {"reason": reason}
    r = api_request(env, "POST", f"/v1/billing/subscriptions/{subscription_id}/cancel", token, json_body=body)
    if dump_raw:
        dump_response(f"new_cancel_subscription:{subscription_id}", r)
    if r.status_code != 204:
        raise RuntimeError(f"[new] cancel {subscription_id} failed: {r.status_code} {r.text}")


# =============================
# CLI / main
# =============================
def summarize_old(a: Dict[str, Any]) -> Tuple[str, str]:
    return (a.get("id", ""), a.get("state", ""))


def summarize_new(s: Dict[str, Any]) -> Tuple[str, str]:
    return (s.get("id", ""), s.get("status", ""))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--env", choices=["sandbox", "live"], default="sandbox")
    p.add_argument("--list", action="store_true", help="Print parsed list output (IDs/status)")
    p.add_argument("--cancel-all", action="store_true", help="Cancel everything discovered (old + new)")
    p.add_argument("--dry-run", action="store_true", help="Show what would be cancelled, but do not cancel")
    p.add_argument("--reason", default="Cancelled via script", help="Reason/note passed to cancel endpoints")
    p.add_argument("--dump-raw", action="store_true", help="Dump raw HTTP responses (status/headers/body)")
    p.add_argument("--page-size", type=int, default=20, help="New mode paging")
    p.add_argument("--new-statuses", default=None, help="New mode filter, e.g. ACTIVE,SUSPENDED")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if PAYPAL_CLIENT_ID.startswith("PUT_") or PAYPAL_CLIENT_SECRET.startswith("PUT_"):
        print("ERROR: Edit PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET first.", file=sys.stderr)
        return 2

    token = get_access_token(args.env, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, dump_raw=args.dump_raw)

    # Attempt BOTH. For personal accounts, either/both may fail or return empty. [web:40][web:10]
    old_items: List[Dict[str, Any]] = []
    new_items: List[Dict[str, Any]] = []

    old_error: Optional[str] = None
    new_error: Optional[str] = None

    try:
        old_items = old_list_billing_agreements(args.env, token, dump_raw=args.dump_raw)
    except Exception as e:
        old_error = str(e)

    try:
        new_items = new_list_subscriptions(
            args.env, token, page_size=args.page_size, statuses=args.new_statuses, dump_raw=args.dump_raw
        )
    except Exception as e:
        new_error = str(e)

    if args.list:
        print("\n== Parsed results ==")
        if old_error:
            print(f"[old] ERROR: {old_error}")
        else:
            print(f"[old] found {len(old_items)} billing agreements")
            for a in old_items:
                _id, state = summarize_old(a)
                if _id:
                    print(f"  [old] {_id} state={state}")

        if new_error:
            print(f"[new] ERROR: {new_error}")
        else:
            print(f"[new] found {len(new_items)} subscriptions")
            for s in new_items:
                _id, status = summarize_new(s)
                if _id:
                    print(f"  [new] {_id} status={status}")

    if args.cancel_all:
        print("\n== Cancel ==")
        if old_error is None:
            for a in old_items:
                agreement_id = a.get("id")
                if not agreement_id:
                    continue
                print(f"[old] cancel {agreement_id}")
                if not args.dry_run:
                    old_cancel_billing_agreement(args.env, token, agreement_id, args.reason, dump_raw=args.dump_raw)

        if new_error is None:
            for s in new_items:
                subscription_id = s.get("id")
                if not subscription_id:
                    continue
                print(f"[new] cancel {subscription_id}")
                if not args.dry_run:
                    new_cancel_subscription(args.env, token, subscription_id, args.reason, dump_raw=args.dump_raw)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## What will likely happen (personal payer account)

- `GET /v1/billing/subscriptions` is documented as “List all subscriptions for merchant account”, so it may not show payer-side “things I’m paying” unless those were created under credentials that have merchant visibility.[2]
- If the API approach doesn’t surface your payer-side automatic payments, PayPal’s supported path is to manage them in the UI under “Automatic payments” (Settings → Payments → Manage automatic payments).[3]

If you run `--dump-raw --list` and paste the two list-call responses (with tokens removed), it’s possible to tell whether it’s a permission/scope issue vs. simply “not exposed for payer accounts.”

## Citations (Part 4)

[1] [Billing Agreements - PayPal Developer](https://developer.paypal.com/docs/api/payments.billing-agreements/v1/)
[2] [Subscriptions - PayPal Developer](https://developer.paypal.com/docs/api/subscriptions/v1/)
[3] [Automatic Payment | Update Recurring Payments](https://www.paypal.com/us/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[4] [Billing Plans - PayPal Developer](https://developer.paypal.com/docs/api/payments.billing-plans/v1/)
[5] [Payments - PayPal Developer](https://developer.paypal.com/docs/api/payments/v1/)
[6] [Paypal Sandbox How to Check Billing Plans and Billing Agreements](https://stackoverflow.com/questions/43929972/paypal-sandbox-how-to-check-billing-plans-and-billing-agreements)
[7] [Count active subscriptions with PayPal API? - Stack Overflow](https://stackoverflow.com/questions/51810180/count-active-subscriptions-with-paypal-api)
[8] [How to Manage Payment Methods in Paypal](https://help.offsec.com/hc/en-us/articles/26763331186580-How-to-Manage-Payment-Methods-in-Paypal)
[9] [PayPal billing agreements | Adobe Commerce - Experience League](https://experienceleague.adobe.com/en/docs/commerce-admin/stores-sales/payments/paypal/paypal-billing-agreements)
[10] [Merchant Subscription FAQs | PayPal GB](https://www.paypal.com/uk/cshelp/article/merchant-subscription-faqs-help289)
[11] [How to Set Up Automatic Payments on PayPal](https://www.youtube.com/watch?v=kCdcMNX65AA)
[12] [[PDF] PayPal Initiate billing agreement](https://verifone.cloud/print/pdf/node/1018)
[13] [PayPal Subscriptions: Tailored Billing for Every Customer](https://developer.paypal.com/docs/subscriptions/)
[14] [Billing agreements use cases - PayPal Developer](https://developer.paypal.com/api/rest/integration/orders-api/api-use-cases/billing-agreements/)
[15] [Integrate Subscriptions for Billing - PayPal Developer](https://developer.paypal.com/docs/multiparty/subscriptions/integrate/)
[16] [What is an Automatic Payment and How Do I Update or Cancel One?](https://www.youtube.com/watch?v=iCAsYepygcQ)
[17] [PayPal v1 - PAYONE Documentation Platform](https://docs.payone.com/payment-methods/paypal/paypal-v1)
[18] [Enabling Subscriptions with PayPal - Support Guides - BlueSnap](https://support.bluesnap.com/docs/enabling-subscriptions-with-paypal)
[19] [How to Disable automatic payments on PayPal - Automatic payments cancel](https://www.youtube.com/watch?v=uVIy7R6g2z0)
[20] [Integrate Subscriptions to Bill Customers Regularly](https://developer.paypal.com/docs/subscriptions/integrate/)

---

## Let's rethink this then. Can we maybe use Playwright to automate it through the PayPal Web UI? Happy to feed it valid auth cookies

Yes—Playwright UI automation is the most practical route for a **personal (payer) PayPal account** because PayPal’s help flow for “Automatic payments” is explicitly a web-settings journey (Settings → Payments → Automatic payments → select merchant → stop/cancel). The “list all subscriptions for merchant account” API endpoint is merchant-scoped, so it’s often the wrong tool for payer-side cleanup.\[1\]\[2\]

## Caveats (so it doesn’t bite later)

- UI selectors in PayPal change regularly, so the script should rely on URLs + resilient locators (roles/text) and should support a **dry-run** mode first.[1]
- Feeding auth cookies can work, but it’s safer to load a persistent browser profile (`launch_persistent_context`) so PayPal’s anti-bot and extra prompts are less likely to trigger than a fresh context every run.\[1\]

## Playwright script (cookie-friendly)

This script:

- Navigates directly to the Automatic Payments page (often reachable as `/myaccount/autopay`).\[3\]\[1\]
- Lists merchants (best-effort).
- Iterates each merchant, tries to find “Cancel/Stop paying with PayPal/Unlink” style actions, confirms, and returns.
- Adds `--cookies cookies.json` (optional) and `--dump-html` / `--trace` / `--screenshot-dir` for debugging.

```python
#!/usr/bin/env python3
"""
paypal_autopay_cleanup.py

Automate PayPal "Automatic payments" cleanup via the web UI using Playwright.

PayPal's documented path is:
  Settings -> Payments -> Automatic payments -> select merchant -> cancel/stop [web:74]

This script tries to go directly to:
  https://www.paypal.com/myaccount/autopay  (commonly used entry point) [web:77][web:74]

Install:
  pip install playwright
  playwright install chromium

Cookies:
  Provide a cookies.json exported in Playwright storage_state format (recommended),
  or as a list of cookie dicts (fallback; see notes in code).

Examples:
  python paypal_autopay_cleanup.py --country uk --dry-run --headful
  python paypal_autopay_cleanup.py --country uk --cookies paypal_state.json --cancel-all --headful
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError


AUTOPAY_PATH = "/myaccount/autopay"  # commonly referenced entry [web:77]


def paypal_base(country: str) -> str:
    # PayPal often localizes, but /myaccount/autopay typically works cross-locale. [web:74]
    if country.lower() == "uk":
        return "https://www.paypal.com"
    return "https://www.paypal.com"


def load_storage_state(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(p: Optional[str]) -> Optional[Path]:
    if not p:
        return None
    d = Path(p)
    d.mkdir(parents=True, exist_ok=True)
    return d


def safe_slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80] or "item"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--country", default="uk", choices=["uk", "us", "other"])
    ap.add_argument("--headful", action="store_true", help="Run with visible browser")
    ap.add_argument("--dry-run", action="store_true", help="Do not click final confirm actions")
    ap.add_argument("--cancel-all", action="store_true", help="Attempt to cancel every automatic payment found")
    ap.add_argument("--cookies", default=None, help="Path to Playwright storage_state JSON (recommended)")
    ap.add_argument("--user-data-dir", default=None, help="Persistent Chromium profile dir (more robust than cookies)")
    ap.add_argument("--dump-html", action="store_true", help="Dump current page HTML on failures")
    ap.add_argument("--screenshot-dir", default=None, help="Write screenshots here on failures")
    ap.add_argument("--trace", action="store_true", help="Enable Playwright tracing (writes trace.zip)")
    args = ap.parse_args()

    base = paypal_base(args.country)
    autopay_url = f"{base}{AUTOPAY_PATH}"

    screenshot_dir = ensure_dir(args.screenshot_dir)

    with sync_playwright() as p:
        browser_type = p.chromium

        context_kwargs: Dict[str, Any] = {}
        if args.cookies:
            # Playwright storage_state format is easiest. If you only have raw cookies,
            # convert them to storage_state or use a persistent profile. (No claim of PayPal support implied.) [web:74]
            context_kwargs["storage_state"] = load_storage_state(args.cookies)

        if args.user_data_dir:
            context = browser_type.launch_persistent_context(
                args.user_data_dir,
                headless=not args.headful,
                viewport={"width": 1400, "height": 900},
            )
        else:
            browser = browser_type.launch(headless=not args.headful)
            context = browser.new_context(viewport={"width": 1400, "height": 900}, **context_kwargs)

        if args.trace:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()

        def fail_artifacts(tag: str) -> None:
            if screenshot_dir:
                page.screenshot(path=str(screenshot_dir / f"{tag}.png"), full_page=True)
            if args.dump_html:
                html = page.content()
                Path(f"{tag}.html").write_text(html, encoding="utf-8")

        # 1) Go to Automatic Payments page (expects to be logged-in already via cookies/profile). [web:74]
        page.goto(autopay_url, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)

        # If not logged in, PayPal will redirect to login.
        if "login" in page.url:
            print(f"Not logged in (redirected to {page.url}). Provide cookies or a persistent profile.")
            fail_artifacts("not_logged_in")
            return 3

        print(f"Opened: {page.url}")

        # 2) Best-effort: identify merchant entries in the left list.
        # PayPal UI shifts; use broad strategies with ARIA roles/text.
        # Typical flow is: list on left, details on right. [web:74]
        try:
            page.get_by_text("Automatic payments", exact=False).first.wait_for(timeout=10_000)
        except PWTimeoutError:
            print("Could not confirm 'Automatic payments' page text; continuing best-effort.")
            fail_artifacts("autopay_page_unconfirmed")

        # Candidate selectors for merchant list items.
        merchant_locators = [
            page.get_by_role("link"),            # many entries are links
            page.get_by_role("button"),          # sometimes entries are buttons
            page.locator("[data-testid] a"),     # heuristic
        ]

        # Collect unique clickable elements with non-empty text.
        candidates: List[Dict[str, Any]] = []
        seen = set()

        for loc in merchant_locators:
            count = min(loc.count(), 400)
            for i in range(count):
                el = loc.nth(i)
                try:
                    txt = (el.inner_text(timeout=200) or "").strip()
                except Exception:
                    continue
                if not txt or len(txt) > 80:
                    continue
                key = txt
                if key in seen:
                    continue
                # Filter out obvious nav items
                if txt.lower() in {"help", "logout", "log out", "settings", "wallet", "summary"}:
                    continue
                seen.add(key)
                candidates.append({"text": txt, "locator": el})

        # Heuristic: PayPal autopay merchant list is usually not huge; show what was detected.
        print(f"Detected {len(candidates)} clickable text candidates (heuristic).")
        if not candidates:
            print("No candidates found; UI likely changed. Use --dump-html/--screenshot-dir for debugging.")
            fail_artifacts("no_candidates")
            return 4

        if not args.cancel_all:
            print("\nNot cancelling (use --cancel-all). Listing detected candidates only:")
            for c in candidates[:80]:
                print(f" - {c['text']}")
            return 0

        # 3) Iterate and try to cancel each
        cancelled = 0
        attempted = 0

        for c in candidates:
            name = c["text"]
            el = c["locator"]
            attempted += 1
            tag = safe_slug(name)

            try:
                el.click(timeout=1500)
                page.wait_for_timeout(1200)

                # Look for cancel / stop paying controls.
                # PayPal help describes cancel from this merchant detail view. [web:74]
                cancel_buttons = [
                    page.get_by_role("button", name=re.compile(r"cancel", re.I)),
                    page.get_by_role("button", name=re.compile(r"stop paying", re.I)),
                    page.get_by_role("button", name=re.compile(r"unlink", re.I)),
                ]

                clicked_cancel = False
                for b in cancel_buttons:
                    if b.count() > 0:
                        try:
                            b.first.click(timeout=1500)
                            clicked_cancel = True
                            break
                        except Exception:
                            pass

                if not clicked_cancel:
                    print(f"[skip] {name}: no cancel/stop/unlink button found")
                    continue

                page.wait_for_timeout(800)

                # Confirm modal/button (varies). Try common confirm verbs.
                confirm_buttons = [
                    page.get_by_role("button", name=re.compile(r"stop", re.I)),
                    page.get_by_role("button", name=re.compile(r"confirm", re.I)),
                    page.get_by_role("button", name=re.compile(r"yes", re.I)),
                    page.get_by_role("button", name=re.compile(r"done", re.I)),
                ]

                if args.dry_run:
                    print(f"[dry-run] Would confirm cancellation for: {name}")
                    fail_artifacts(f"dryrun_{tag}")
                    continue

                confirmed = False
                for b in confirm_buttons:
                    if b.count() > 0:
                        try:
                            b.first.click(timeout=2000)
                            confirmed = True
                            break
                        except Exception:
                            pass

                if not confirmed:
                    print(f"[warn] {name}: clicked cancel but couldn't find confirm; capturing artifacts")
                    fail_artifacts(f"no_confirm_{tag}")
                    continue

                cancelled += 1
                print(f"[ok] cancelled: {name}")
                page.wait_for_timeout(1200)

            except Exception as e:
                print(f"[err] {name}: {e}")
                fail_artifacts(f"err_{tag}")
                continue

        print(f"\nAttempted: {attempted}, cancelled: {cancelled}")

        if args.trace:
            context.tracing.stop(path="trace.zip")

        context.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Getting cookies into Playwright (practical options)

- Preferred: use Playwright once interactively with `--user-data-dir ./pprof --headful`, log in, then rerun headless with the same profile directory (more stable than raw cookies).[1]
- If you truly want to “feed cookies”, export **Playwright storage_state** JSON from an authenticated context and pass it with `--cookies paypal_state.json` (the script expects that structure).[1]

What format can you provide the auth material in: Playwright `storage_state.json`, Netscape cookie jar, or raw `Cookie:` header string?

## Citations (Part 5)

[1] [Automatic Payment | Update Recurring Payments](https://www.paypal.com/uk/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[2] [Subscriptions - PayPal Developer](https://developer.paypal.com/docs/api/subscriptions/v1/)
[3] [How To Cancel PayPal Automatic Pre-Approved Payments (Autopay) And Reoccurring Subscriptions](https://www.youtube.com/watch?v=bSNHpWG3SPs)
[4] [Automatic Payment | Update Recurring Payments](https://www.paypal.com/us/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[5] [How to Cancel Automatic Payments on PayPal](https://www.freshbooks.com/hub/payments/how-to-cancel-a-recurring-payment-on-paypal)
[6] [How to CANCEL PayPal Subscription or Recurring / Automatic Payments in 2023](https://www.youtube.com/watch?v=aFvm-k_ZFUo)
[7] [How To Cancel PreApproved Paypal Payments 2023 - YouTube](https://www.youtube.com/watch?v=KDm9D1jWEgE)
[8] [How to Manage Payment Methods in Paypal](https://help.offsec.com/hc/en-us/articles/26763331186580-How-to-Manage-Payment-Methods-in-Paypal)
[9] [How to Disable automatic payments on PayPal - Automatic payments cancel](https://www.youtube.com/watch?v=uVIy7R6g2z0)
[10] [Automatic Payments - PayPal](https://www.paypal.com/hk/webapps/mpp/automatic-payments)
[11] [How to Set Up Automatic Payments on PayPal](https://www.youtube.com/watch?v=kCdcMNX65AA)
[12] [What is an Automatic Payment and How Do I Update or Cancel One?](https://www.youtube.com/watch?v=iCAsYepygcQ)
[13] [How To Cancel Pre Approved Payments In Paypal - YouTube](https://www.youtube.com/watch?v=IL7nO1LNJpU)
[14] [Everything About PayPal Automatic Payments](https://www.saasant.com/blog/paypal-automatic-payments/)
[15] [PayPal Community](https://www.paypal-community.com/t5/Transactions/How-to-disable-entirely-the-automatic-payment-feature/td-p/3090814/page/2)
[16] [How to Cancel an Automatic PayPal Subscription - Netcetera](https://help.netcetera.co.uk/knowledgebase/article/how-to-cancel-an-automatic-paypal-subscription)
[17] [Change Automatic Payment Settings in PayPal Account | Tutorial](https://www.youtube.com/watch?v=yiyXv3pwNCE)
[18] [How To Cancel PayPal Automatic Payments 2025 Disable PayPal](https://www.youtube.com/watch?v=v2YzaStr_mg)
[19] [How to Cancel Pre Approved Subscription Payments on PayPal](https://www.facebook.com/dcpwebdesigners/videos/how-to-cancel-pre-approved-subscription-payments-on-paypal-2020-update/620506718859539/)
[20] [www.paypal.com › cshelp › article › what-is-an-automatic-payment-and-h...](https://www.paypal.com/bb/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[21] [Managing Automatic Payments](https://www.reddit.com/r/paypal/comments/1ak7rz0/managing_automatic_payments/)

---

## If I can use Playwright head fully and manually log in, that's fine

Yes—do it headful once, log in manually, then reuse the same persistent browser profile so Playwright stays authenticated across runs via `launch_persistent_context(user_data_dir, ...)`. That avoids fiddling with cookies and is the most reliable approach for a site like PayPal.\[1\]\[2\]\[3\]

## Workflow

1. Install + browser runtime:

- `pip install playwright`
- `playwright install chromium`

1. First run (interactive login, no cancelling):

- `python paypal_autopay_cleanup.py --headful --user-data-dir ./pprof --list-only`

1. Second run (still headful for safety, but now logged in already):

- `python paypal_autopay_cleanup.py --headful --user-data-dir ./pprof --dry-run --cancel-all`

1. Final run (actually cancel):

- `python paypal_autopay_cleanup.py --headful --user-data-dir ./pprof --cancel-all`

PayPal’s own help flow indicates the target page is the “Automatic payments” management area (Settings → Payments → Manage automatic payments).[3]

## Script (persistent profile + manual login)

This version:

- Always uses a persistent profile (required flag), which is what makes login stick.\[2\]\[1\]
- Has a `--list-only` mode and a `--dump-raw` mode (screenshots + HTML dump) to debug selector drift.
- Navigates to `/myaccount/autopay` as the main entry point and falls back to printing the current URL if redirected.[3]

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

AUTOPAY_URL = "https://www.paypal.com/myaccount/autopay"  # entry to manage automatic payments. [web:74]


def ensure_dir(p: Optional[str]) -> Optional[Path]:
    if not p:
        return None
    d = Path(p)
    d.mkdir(parents=True, exist_ok=True)
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user-data-dir", required=True, help="Persistent Chromium profile dir (keeps you logged in)")
    ap.add_argument("--headful", action="store_true", help="Show the browser window")
    ap.add_argument("--list-only", action="store_true", help="Only list detected merchants; do not cancel")
    ap.add_argument("--cancel-all", action="store_true", help="Attempt to cancel every automatic payment found")
    ap.add_argument("--dry-run", action="store_true", help="Go through clicks but stop before final confirm")
    ap.add_argument("--dump-raw", action="store_true", help="On failures: dump HTML + screenshot")
    ap.add_argument("--artifact-dir", default="./artifacts", help="Where to write screenshots/HTML if --dump-raw")
    args = ap.parse_args()

    artifact_dir = ensure_dir(args.artifact_dir) if args.dump_raw else None

    with sync_playwright() as p:
        # Persistent auth: user_data_dir stores cookies/local storage etc. [web:88][web:97]
        context = p.chromium.launch_persistent_context(
            args.user_data_dir,
            headless=not args.headful,
            viewport={"width": 1400, "height": 900},
        )
        page = context.new_page()

        def snap(tag: str) -> None:
            if not artifact_dir:
                return
            page.screenshot(path=str(artifact_dir / f"{tag}.png"), full_page=True)
            (artifact_dir / f"{tag}.html").write_text(page.content(), encoding="utf-8")

        page.goto(AUTOPAY_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)

        # If redirected to login, user can log in manually and re-run or just continue after login.
        if "login" in page.url.lower():
            print(f"Redirected to login: {page.url}")
            print("Log in manually in the opened browser, then press Enter here to continue...")
            input()
            page.goto(AUTOPAY_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)

        print(f"Now at: {page.url}")

        # Confirm we're on the right general area (best-effort; UI changes).
        try:
            page.get_by_text(re.compile(r"automatic payments", re.I)).first.wait_for(timeout=10_000)
        except PWTimeoutError:
            print("Could not positively identify the Automatic Payments page text (UI may differ).")
            if args.dump_raw:
                snap("autopay_not_detected")

        # Heuristic: on this page there is typically a list of merchants; try to collect clickable entries.
        # Using role=link/button catches most list UIs without depending on brittle CSS.
        merchant_candidates = []
        for loc in (page.get_by_role("link"), page.get_by_role("button")):
            for i in range(min(loc.count(), 300)):
                el = loc.nth(i)
                try:
                    txt = (el.inner_text(timeout=200) or "").strip()
                except Exception:
                    continue
                if not txt or len(txt) > 80:
                    continue
                if re.search(r"(help|logout|log out|settings|wallet|summary)", txt, re.I):
                    continue
                merchant_candidates.append((txt, el))

        # De-dupe by text
        seen = set()
        merchants = []
        for txt, el in merchant_candidates:
            if txt in seen:
                continue
            seen.add(txt)
            merchants.append((txt, el))

        print(f"Detected {len(merchants)} merchant candidates.")
        for txt, _ in merchants[:100]:
            print(f" - {txt}")

        if args.list_only:
            context.close()
            return 0

        if not args.cancel_all:
            print("Nothing cancelled (pass --cancel-all).")
            context.close()
            return 0

        cancelled = 0
        for name, el in merchants:
            try:
                el.click(timeout=2000)
                page.wait_for_timeout(1200)

                # Try several likely labels for the “stop/cancel” action.
                # PayPal’s help flow describes selecting the merchant then cancelling/stopping. [web:74]
                cancel_btn = (
                    page.get_by_role("button", name=re.compile(r"cancel", re.I)).first
                    if page.get_by_role("button", name=re.compile(r"cancel", re.I)).count() > 0
                    else None
                )
                if not cancel_btn:
                    for pat in (r"stop paying", r"unlink", r"remove"):
                        loc = page.get_by_role("button", name=re.compile(pat, re.I))
                        if loc.count() > 0:
                            cancel_btn = loc.first
                            break

                if not cancel_btn:
                    print(f"[skip] {name}: no cancel/stop button found")
                    continue

                cancel_btn.click(timeout=2000)
                page.wait_for_timeout(800)

                if args.dry_run:
                    print(f"[dry-run] {name}: reached cancel flow; not confirming")
                    if args.dump_raw:
                        snap(f"dryrun_{re.sub('[^a-z0-9]+','_',name.lower())[:60]}")
                    continue

                # Confirm button in modal/dialog
                confirm = None
                for pat in (r"confirm", r"yes", r"stop", r"cancel payment", r"done"):
                    loc = page.get_by_role("button", name=re.compile(pat, re.I))
                    if loc.count() > 0:
                        confirm = loc.first
                        break

                if not confirm:
                    print(f"[warn] {name}: cancel clicked but confirm button not found")
                    if args.dump_raw:
                        snap(f"no_confirm_{re.sub('[^a-z0-9]+','_',name.lower())[:60]}")
                    continue

                confirm.click(timeout=2000)
                page.wait_for_timeout(1200)
                cancelled += 1
                print(f"[ok] cancelled: {name}")

            except Exception as e:
                print(f"[err] {name}: {e}")
                if args.dump_raw:
                    snap(f"err_{re.sub('[^a-z0-9]+','_',name.lower())[:60]}")
                continue

        print(f"Cancelled: {cancelled}")
        context.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

What OS/browser are you running this on (Linux/macOS/Windows), and do you want it to target Chromium only or also try Firefox/WebKit?

## Citations (Part 6)

[1] [Authentication](https://playwright.bootcss.com/python/docs/auth)
[2] [BrowserType | Playwright Python](https://playwright.dev/python/docs/api/class-browsertype)
[3] [Automatic Payment | Update Recurring Payments](https://www.paypal.com/uk/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[4] [Saving Login with Playwright - python](https://stackoverflow.com/questions/74520727/saving-login-with-playwright)
[5] [[Bug]: Session cookies not persisting in ` ...](https://github.com/microsoft/playwright/issues/36139)
[6] [Authentication | Playwright Python](https://www.cuketest.com/playwright/python/docs/auth/)
[7] [Python playwright won't let me open user profile other than ...](https://stackoverflow.com/questions/74951776/python-playwright-wont-let-me-open-user-profile-other-than-default-profile)
[8] [Store authentication state across Playwright tests in applications that ...](https://frontendrescue.com/posts/2023-07-28-session-storage-playwright)
[9] [How to Manage Payment Methods in Paypal](https://help.offsec.com/hc/en-us/articles/26763331186580-How-to-Manage-Payment-Methods-in-Paypal)
[10] [Use launch_persistent_context in Playwright Python With Examples](https://www.lambdatest.com/automation-testing-advisor/python/playwright-python-launch_persistent_context)
[11] [Authentication | Playwright Python](https://playwright.dev/python/docs/auth)
[12] [Automatic Payment | Update Recurring Payments](https://www.paypal.com/us/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[13] [Launch persistent context from current directory in playwright](https://stackoverflow.com/questions/73338944/launch-persistent-context-from-current-directory-in-playwright)
[14] [Authentication](https://playwright.dev/docs/auth)
[15] [How to Set Up Automatic Payments on PayPal](https://www.youtube.com/watch?v=kCdcMNX65AA)
[16] [How to Maintain Authentication State in Playwright](https://roundproxies.com/blog/authentication-playwright/)
[17] [What is an Automatic Payment and How Do I Update or Cancel One?](https://www.youtube.com/watch?v=iCAsYepygcQ)
[18] [Automating Chrome with Existing Profiles using Playwright ...](https://www.neovasolutions.com/2024/06/13/automating-chrome-with-existing-profiles-using-playwright-and-typescript/)
[19] [#35 Playwright with Python | Reuse authenticated state using storage file](https://www.youtube.com/watch?v=JMq8ImhDih0)
[20] [Everything About PayPal Automatic Payments](https://www.saasant.com/blog/paypal-automatic-payments/)
[21] [Release notes | Playwright Python](https://playwright.dev/python/docs/release-notes)

---

## MacOS. Chromium only is fine, this is only getting run once

On macOS, the smoothest one-shot approach is: run Playwright **headful** with a persistent `--user-data-dir`, log in manually once, then let the script click through “Automatic payments” and cancel entries.\[1\]\[2\]

## How to run (macOS, Chromium)

1. Install:

- `python3 -m pip install playwright`
- `python3 -m playwright install chromium`\[3\]\[4\]

1. First pass (login + list only):

- `python3 paypal_autopay_cleanup.py --headful --user-data-dir ./pprof --list-only`

1. Dry-run cancel (no final confirm):

- `python3 paypal_autopay_cleanup.py --headful --user-data-dir ./pprof --cancel-all --dry-run --dump-raw`

1. Real cancel:

- `python3 paypal_autopay_cleanup.py --headful --user-data-dir ./pprof --cancel-all --dump-raw`

PayPal’s help page confirms the manual flow is Settings → Payments → Automatic payments → select merchant → cancel.[1]

## Script (Chromium-only, manual login)

This version is tuned for your “run once” use case and only uses Chromium persistent context.[2]

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

AUTOPAY_URL = "https://www.paypal.com/myaccount/autopay"  # entry point to automatic payments area. [web:74]


def ensure_dir(p: str) -> Path:
    d = Path(p)
    d.mkdir(parents=True, exist_ok=True)
    return d


def slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return (s[:60] or "item").strip("_")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user-data-dir", required=True, help="Persistent Chromium profile dir (keeps you logged in).")
    ap.add_argument("--headful", action="store_true", help="Show the browser window.")
    ap.add_argument("--list-only", action="store_true", help="Only list merchant candidates; no cancelling.")
    ap.add_argument("--cancel-all", action="store_true", help="Attempt to cancel every automatic payment found.")
    ap.add_argument("--dry-run", action="store_true", help="Proceed until confirm step, but do not confirm.")
    ap.add_argument("--dump-raw", action="store_true", help="On warnings/errors: save HTML + screenshot.")
    ap.add_argument("--artifact-dir", default="./artifacts", help="Where to write screenshots/HTML when --dump-raw.")
    args = ap.parse_args()

    artifacts = ensure_dir(args.artifact_dir) if args.dump_raw else None

    with sync_playwright() as p:
        # launch_persistent_context keeps session state in user_data_dir. [web:97]
        context = p.chromium.launch_persistent_context(
            args.user_data_dir,
            headless=not args.headful,
            viewport={"width": 1400, "height": 900},
        )
        page = context.new_page()

        def capture(tag: str) -> None:
            if not artifacts:
                return
            page.screenshot(path=str(artifacts / f"{tag}.png"), full_page=True)
            (artifacts / f"{tag}.html").write_text(page.content(), encoding="utf-8")

        # Navigate to autopay page; if redirected to login, user logs in manually, then continue. [web:74]
        page.goto(AUTOPAY_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)

        if "login" in page.url.lower():
            print(f"Redirected to login: {page.url}")
            print("Log in manually (including any 2FA), then press Enter here...")
            input()
            page.goto(AUTOPAY_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)

        print(f"Now at: {page.url}")

        # Best-effort confirmation we’re in the right place (text varies by locale). [web:74]
        try:
            page.get_by_text(re.compile(r"automatic payments", re.I)).first.wait_for(timeout=10_000)
        except PWTimeoutError:
            print("Could not confirm 'Automatic payments' text; continuing best-effort.")
            capture("autopay_unconfirmed")

        # Heuristic: collect clickable merchant entries (UI changes often).
        candidates = []
        for loc in (page.get_by_role("link"), page.get_by_role("button")):
            for i in range(min(loc.count(), 400)):
                el = loc.nth(i)
                try:
                    txt = (el.inner_text(timeout=200) or "").strip()
                except Exception:
                    continue
                if not txt or len(txt) > 80:
                    continue
                if re.search(r"(help|logout|log out|settings|wallet|summary)", txt, re.I):
                    continue
                candidates.append((txt, el))

        # De-dupe by label
        seen = set()
        merchants = []
        for txt, el in candidates:
            if txt in seen:
                continue
            seen.add(txt)
            merchants.append((txt, el))

        print(f"Detected {len(merchants)} merchant candidates:")
        for txt, _ in merchants[:120]:
            print(f" - {txt}")

        if args.list_only:
            context.close()
            return 0

        if not args.cancel_all:
            print("Nothing cancelled (pass --cancel-all).")
            context.close()
            return 0

        cancelled = 0
        for name, el in merchants:
            tag = slug(name)
            try:
                el.click(timeout=2500)
                page.wait_for_timeout(1200)

                # Try common action labels; exact text can vary. [web:74]
                action = None
                for pat in (r"cancel", r"stop paying", r"remove paypal", r"remove", r"unlink"):
                    loc = page.get_by_role("button", name=re.compile(pat, re.I))
                    if loc.count() > 0:
                        action = loc.first
                        break

                if not action:
                    print(f"[skip] {name}: no cancel/stop/remove/unlink button found")
                    continue

                action.click(timeout=2500)
                page.wait_for_timeout(800)

                if args.dry_run:
                    print(f"[dry-run] {name}: reached cancel flow; not confirming")
                    capture(f"dryrun_{tag}")
                    continue

                confirm = None
                for pat in (r"confirm", r"yes", r"stop", r"cancel automatic", r"done", r"remove"):
                    loc = page.get_by_role("button", name=re.compile(pat, re.I))
                    if loc.count() > 0:
                        confirm = loc.first
                        break

                if not confirm:
                    print(f"[warn] {name}: confirm button not found after opening cancel flow")
                    capture(f"no_confirm_{tag}")
                    continue

                confirm.click(timeout=2500)
                page.wait_for_timeout(1200)
                cancelled += 1
                print(f"[ok] cancelled: {name}")

            except Exception as e:
                print(f"[err] {name}: {e}")
                capture(f"err_{tag}")
                continue

        print(f"Cancelled: {cancelled}")
        context.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Safety tip

Run with `--dry-run --dump-raw` first so you can visually confirm it’s clicking the right buttons before it does irreversible cancels.[1]

If you paste a screenshot of your “Automatic payments” page (with names/amounts blurred), the selectors can be tightened so it only targets the merchant list panel rather than “random links/buttons.”

## Citations (Part 7)

[1] [Automatic Payment | Update Recurring Payments](https://www.paypal.com/uk/cshelp/article/what-is-an-automatic-payment-and-how-do-i-update-or-cancel-one-help240)
[2] [BrowserType | Playwright Python](https://playwright.dev/python/docs/api/class-browsertype)
[3] [Browsers](https://playwright.dev/docs/browsers)
[4] [Installation](https://playwright.dev/docs/intro)
[5] [Installing Chromium for Playwright on Mac - Technoverse](https://technoverse.id/en/2024/12/installing-chromium-for-playwright-on-mac/)
[6] [How to use installed version of chrome in Playwright?](https://stackoverflow.com/questions/62281859/how-to-use-installed-version-of-chrome-in-playwright)
[7] [Playwright does not support chromium on mac12 - arm-64 · Issue #13964 · microsoft/playwright](https://github.com/microsoft/playwright/issues/13964)
[8] [Use launch_persistent_context in Playwright Python With Examples](https://www.lambdatest.com/automation-testing-advisor/python/playwright-python-launch_persistent_context)
[9] [How to Cancel Automatic Payments on PayPal - FreshBookswww.freshbooks.com › hub › how-to-cancel-a-recurring-payment-on-paypal](https://www.freshbooks.com/hub/payments/how-to-cancel-a-recurring-payment-on-paypal)
[10] [Installation](https://playwright.bootcss.com/python/docs/installation)
[11] [Chrome extensions | Playwright Python](https://playwright.dev/python/docs/chrome-extensions)
[12] [How To Cancel Recurring Payments On PayPal](https://paymattic.com/how-to-cancel-recurring-payments-on-paypal/)
[13] [Playwright: how to connect existing chromium browser in MacBook](https://stackoverflow.com/questions/78948271/playwright-how-to-connect-existing-chromium-browser-in-macbook)
[14] [Automating Chrome with Existing Profiles using Playwright and ...](https://www.neovasolutions.com/2024/06/13/automating-chrome-with-existing-profiles-using-playwright-and-typescript/)
[15] [How to Disable automatic payments on PayPal - Automatic payments cancel](https://www.youtube.com/watch?v=uVIy7R6g2z0)
[16] [[BUG] Failed to launch chromium because executable ...](https://github.com/microsoft/playwright/issues/4033)
[17] [[Bug]: launch_persistent_context hangs when started with ... - GitHub](https://github.com/microsoft/playwright/issues/31769)
[18] [Installation | Playwright 中文文档](https://playwright.bootcss.com/docs/installation)
[19] [How to cancel automatic PayPal subscription?](https://portal.ukbox.co.uk/index.php?rp=%2Fknowledgebase%2F4933%2FHow-to-cancel-automatic-PayPal-subscription.html)
[20] [A Step by Step Guide to Playwright and Chromium!](https://dev.to/joshuaamaju/mastering-website-previews-a-step-by-step-guide-to-playwright-and-chromium-2a8p)
