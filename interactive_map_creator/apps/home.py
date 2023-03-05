import streamlit as st
import logging
import utils

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        sidebar_msg = st.info(
            """
            ### About

            Interactive Map Creator is created and maintained by [@hreikin](https://hreikin.co.uk). The source code is available on [GitHub](https://github.com/hreikin/interactive-map-creator), community contributions are always welcome.
            
            GNU Affero General Public License v3.0 or later: [AGPL v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)
            """
            )
    col_1, col_2 = st.columns(2)
    with col_1:
        st.header(f"*Welcome*, to the Interactive Map Creator.")
        st.markdown(
            """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """
            )
        st.subheader("Getting Started")
        st.markdown(
            """
            Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
            """
            )
    with col_2:
        utils.load_images(utils.home_images)
