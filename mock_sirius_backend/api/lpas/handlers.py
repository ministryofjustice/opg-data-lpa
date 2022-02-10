from ..utilities import load_data

from textwrap import wrap
import logging


def handle_lpa_get(query_params):
    if "merisid" in query_params:

        meris_id = str(query_params["merisid"])
        print(f"using use my lpa with id {meris_id}")

        if meris_id[0] == "2":
            print(f"test_id is a valid meris id: {meris_id}")

            response_data = load_data(
                parent_folder="lpas", filename="use_an_lpa_response.json", as_json=False
            )
            for result in response_data["results"]:
                if result["donor"]["caseRecNumber"] in meris_id:
                    response = [result]
                    return 200, response

        elif len(meris_id) == 3:
            print("oh no you crashed sirius")

            response_code = meris_id

            return response_code, f"Sirius broke bad - error {response_code}"

        else:
            print(f"{meris_id} is not a found in Sirius")
            return 404, ""


    if "lpaonlinetoolid" in query_params:
        lpa_online_tool_id = query_params["lpaonlinetoolid"]
        print(f"using lpa online tool with id {lpa_online_tool_id}")

        if lpa_online_tool_id[0] == "A":
            print(f"test_id is a valid lpa-online-tool id: {lpa_online_tool_id}")

            response_data = load_data(
                parent_folder="lpas",
                filename="lpa_online_tool_response.json",
                as_json=False,
            )

            for result in response_data["results"]:
                if result["onlineLpaId"] in lpa_online_tool_id:
                    response = [result]
                    return 200, response

        elif lpa_online_tool_id[:5] == "crash":
            print("oh no you crashed sirius")

            response_code = lpa_online_tool_id[-3:]

            return response_code, f"Sirius broke bad - error {response_code}"

        else:
            print(f"{lpa_online_tool_id} is not a lpa-online-tool id")
            return 404, ""

    elif "uid" in query_params:
        sirius_uid = str(query_params["uid"])

        print(f"using use my lpa with id {sirius_uid}")

        if sirius_uid[0] == "7":
            print(f"test_id is a valid sirius uid: {sirius_uid}")

            response_data = load_data(
                parent_folder="lpas", filename="use_an_lpa_response.json", as_json=False
            )

            case_id = "-".join(wrap(sirius_uid, 4))

            for result in response_data["results"]:
                if result["uId"] in case_id:
                    response = [result]
                    return 200, response

        elif len(sirius_uid) == 3:
            print("oh no you crashed sirius")

            response_code = sirius_uid

            return response_code, f"Sirius broke bad - error {response_code}"

        else:
            print(f"{sirius_uid} is not a sirius uid")
            return 404, ""


def handle_request_letter(caseUid, actorUid, notes):

    response_data = load_data(
        parent_folder="lpas", filename="use_an_lpa_response.json", as_json=False
    )

    case_id = "-".join(wrap(str(caseUid), 4))
    actor_id = "-".join(wrap(str(actorUid), 4))

    for result in response_data["results"]:
        if result["uId"] in case_id:

            if notes != None:
                return 200, "{\"queuedForCleansing\":true}"

            if result['donor']['uId'] == actor_id:
                return 204, "{}"

            for attorney in result['attorneys']:
                if  attorney['uId'] == actor_id:
                    return 204, "{}"

    return 400, "{}"
