import requests
import streamlit as st

SCRYFALL_API_URL = "https://api.scryfall.com"

def search_to_cardlist(search_string):
    has_more = True
    page = 1
    cards = []
    while has_more:
        response, status_code = _fetch_card_page(search_string, page)
        if status_code == 404:
            print("Could not find any cards matching that...")
            return None
        for card in response['data']:
            print(card['name'])
            cards.append(card['name'])
        page += 1
        has_more = response['has_more']
    return cards

def _fetch_card_page(search_string, page):
    payload = {"q":search_string, "page":page}
    r = requests.get(
        f"{SCRYFALL_API_URL}/cards/search",
        params=payload
    )
    response = r.json()
    return response, r.status_code

st.title("Scryfall to Cardmarket")
st.divider()
scry_search_string = st.text_area("Scryfall search string")
if st.button("Give me a wantlist!"):
    cards = search_to_cardlist(scry_search_string)
    if not cards:
        st.error('No cards found', icon="🚨")
        st.info("""
            Check your search string, and maybe check 
            [syntax guide](https://scryfall.com/docs/syntax) and try again
        """,  icon="ℹ️")
    else:
        st.success(f"{len(cards)} cards found, printing wantlist below",  icon="✅")
        cards_string = "\n".join([ f"1 {x}" for x in cards ])
        st.code(cards_string)
