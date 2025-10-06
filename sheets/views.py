from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.conf import settings
import json
from .google_client import get_sheets_service

# Utility: map row -> dict based on header
# We'll expect the sheet first row to contain headers like:
# id, name, owner_email, role, hp, mp, image_url, notes, created_at, updated_at
# and rows from A2 downward contain values.

HEADER_RANGE = 'Characters!A1:1'  # header row
DATA_RANGE = getattr(settings, "GOOGLE_SHEETS_RANGE", "Characters!A2:Z")

def _get_spreadsheet_id():
    return getattr(settings, "GOOGLE_SHEETS_ID")

def _read_all():
    sheet = get_sheets_service()
    ssid = _get_spreadsheet_id()
    # read header
    header_res = sheet.values().get(spreadsheetId=ssid, range=HEADER_RANGE).execute()
    headers = header_res.get('values', [[]])[0]
    # read data rows
    res = sheet.values().get(spreadsheetId=ssid, range=DATA_RANGE).execute()
    rows = res.get('values', [])
    items = []
    for idx, r in enumerate(rows, start=2):
        obj = {}
        for i, h in enumerate(headers):
            obj[h] = r[i] if i < len(r) else ""
        # add row index to help with updates/deletes
        obj['_row'] = idx
        items.append(obj)
    return headers, items

def _append_row(values):
    sheet = get_sheets_service()
    ssid = _get_spreadsheet_id()
    body = {'values': [values]}
    return sheet.values().append(
        spreadsheetId=ssid,
        range=DATA_RANGE,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

def _update_row(range_a1, values):
    sheet = get_sheets_service()
    ssid = _get_spreadsheet_id()
    body = {'values': [values]}
    return sheet.values().update(
        spreadsheetId=ssid,
        range=range_a1,
        valueInputOption='RAW',
        body=body
    ).execute()

def _clear_row(range_a1):
    sheet = get_sheets_service()
    ssid = _get_spreadsheet_id()
    return sheet.values().clear(spreadsheetId=ssid, range=range_a1).execute()

@csrf_exempt
def characters_api(request):
    """
    GET -> list all characters
    POST -> create new character (body: JSON mapping of headers -> values)
    PUT/PATCH -> update a character (requires _row or id)
    DELETE -> delete a character (requires _row or id)
    """
    if request.method == 'GET':
        headers, items = _read_all()
        return JsonResponse({'headers': headers, 'characters': items})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            return HttpResponseBadRequest('Invalid JSON')
        # ensure headers exist
        headers_res = get_sheets_service().values().get(
            spreadsheetId=_get_spreadsheet_id(), range=HEADER_RANGE
        ).execute()
        headers = headers_res.get('values', [[]])[0]
        # Build a row following headers order
        row = [payload.get(h, '') for h in headers]
        append_res = _append_row(row)
        return JsonResponse({'status': 'ok', 'append': append_res})
    elif request.method in ('PUT', 'PATCH'):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            return HttpResponseBadRequest('Invalid JSON')
        # must provide _row or id
        row_index = payload.get('_row')
        if not row_index:
            return HttpResponseBadRequest('Missing _row (sheet row number to update)')
        # load headers
        headers_res = get_sheets_service().values().get(
            spreadsheetId=_get_spreadsheet_id(), range=HEADER_RANGE
        ).execute()
        headers = headers_res.get('values', [[]])[0]
        row_vals = [payload.get(h, '') for h in headers]
        # compute A1 range for that row, e.g. Characters!A{row}:Z{row}
        # We'll compute the end column by headers length.
        end_col = chr(ord('A') + max(0, len(headers)-1))
        range_a1 = f"Characters!A{row_index}:{end_col}{row_index}"
        update_res = _update_row(range_a1, row_vals)
        return JsonResponse({'status': 'ok', 'update': update_res})
    elif request.method == 'DELETE':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            payload = {}
        row_index = payload.get('_row')
        if not row_index:
            return HttpResponseBadRequest('Missing _row (sheet row number to clear)')
        # To remove a row, we can clear it (or use batchUpdate to delete the row)
        range_a1 = f"Characters!A{row_index}:Z{row_index}"
        clear_res = _clear_row(range_a1)
        return JsonResponse({'status': 'ok', 'clear': clear_res})
    else:
        return HttpResponseNotAllowed(['GET','POST','PUT','PATCH','DELETE'])
