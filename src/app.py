from nicegui import app, ui
from database import queries
import bcrypt

@ui.page('/', dark=True)
def home_page():
    header()
    with ui.column().classes('mx-auto'):
        ui.markdown('# Home Page')
        ui.separator()
        ui.markdown('#### Check out the games, publishers, and genres tab to see games on the website')
        ui.markdown('#### Make an account to post reviews and save games to your library')

@ui.page('/games', dark=True)
def games_page():
    header()
    with ui.column().classes('mx-auto'):
        ui.markdown('# Games Page')
    
        columns =  [
            # name = no clue tbh, label = what the column is called (user sees this), field = key in which we will search for the rows
            {'name': 'title', 'label': 'Title', 'field': 'title'}, # col 1 : title from "title"
            {'name': 'genre', 'label': 'Genre', 'field': 'genre'}, # col 2 : genre from 'genre_name'
            {'name': 'release', 'label': 'Release Date', 'field': 'release_date'}, # col 3 : release date from 'release_date'
            {'name': 'pub', 'label': 'Publisher', 'field': 'publisher'}, # col 4 : publisher from 'pub_name'
            {'name': 'rating', 'label': 'Rating', 'field': 'rating'} # col 5 : rating from avg <- AVG(rating) grouped by distinct games
        ]
        rows = []
    
        games = queries.get_public_games(order='asc')
        for game in games:
            rows.append({'title': game[0], 'genre': game[1],'release_date': game[4], 'publisher': game[2], 'rating': game[3]})
    
        sorting_radio = None
        order_radio = None
    
        def filter_update():
            games = queries.get_public_games(sorting=sorting_radio.value, order=order_radio.value)
            #games_table.remove_rows(rows)
            new_rows = []
            for game in games:
                new_row = {'title': game[0], 'genre': game[1],'release_date': game[4], 'publisher': game[2], 'rating': game[3]}
                new_rows.append(new_row)
            games_table.update_rows(new_rows)
    
        ui.separator().classes('w-128')
        with ui.splitter(limits=(50,50)).classes('mx-auto') as splitter:
            with splitter.before:
                with ui.column().classes('mr-24'):
                    ui.markdown('####Sort Type')
                    sorting_radio = ui.radio(['Title', 'Genre', 'Publisher', 'Release Date', 'Rating'], value='Title', on_change=filter_update)
            with splitter.after:
                with ui.column().classes('ml-24'):
                    ui.markdown('####Order')
                    order_radio = ui.radio(['Ascending', 'Descending'], value='Ascending', on_change=filter_update)
        ui.separator().classes('w-128')
        games_table = ui.table(columns=columns, rows=rows, pagination=10).classes('mx-auto')
    # Text Box Query -> user types text into an input box -> then users than choose a game and see all the reviews for it

@ui.page('/publishers', dark=True)
def publishers_page():
    header()
    with ui.column().classes('mx-auto'):
        ui.markdown('# Publishers Page')
        ui.separator()
        # Display all publishers
        def display_publishers_table():
            publishers = queries.get_publishers()
            c = [
                # name = no clue tbh, label = what the column is called (user sees this), field = key in which we will search for the rows
                {'name': 'name', 'label': 'Name', 'field': 'name'} # col 1 : name of publisher from 'publisher'
            ]
            if publishers:
                r = []
                for pub in publishers:
                    r.append({'name': pub[1]})
                ui.table(columns=c, rows=r, pagination=10).classes('mx-auto')
            else:
                ui.markdown('Error! No publishers found.')
        with ui.tabs().classes('mx-auto') as tabs:
            all_publishers_tab = ui.tab('All Publishers')
            search_publishers_tab = ui.tab('Games by Publisher')
        with ui.tab_panels(tabs, value=all_publishers_tab).classes('w-full mx-auto'):
            with ui.tab_panel(all_publishers_tab).classes('w-full mx-auto'):
                with ui.column().classes('mx-auto w-full'):
                    display_publishers_table()
            with ui.tab_panel(search_publishers_tab).classes('w-full mx-auto'):
                with ui.column().classes('mx-auto w-full'):
                    columns =  [
                        # name = no clue tbh, label = what the column is called (user sees this), field = key in which we will search for the rows
                        {'name': 'title', 'label': 'Title', 'field': 'title'}, # col 1 : title from "title"
                        {'name': 'release', 'label': 'Release Date', 'field': 'release_date'}, # col 2 : release date from 'release_date'
                        {'name': 'genre', 'label': 'Genre', 'field': 'genre'}, # col 3 : genre_name from genres table
                        {'name': 'rating', 'label': 'Rating', 'field': 'rating'} # col 4 : rating from avg <- AVG(rating) grouped by distinct games
                    ]
                    rows = []
                    games = []

                    for game in games:
                        rows.append({'title': game[0], 'genre': game[1], 'release_date': game[4], 'rating': game[3]})
    
                    sorting_radio = None
                    order_radio = None
                    publisher_select_value = {}

                    def filter_update():
                        games = queries.get_games_by_publisher_name(publisher_name = publisher_select_value['publisher'], sorting=sorting_radio.value, order=order_radio.value)
                        new_rows = []
                        for game in games:
                            new_row = {'title': game[0], 'genre': game[1], 'release_date': game[4], 'rating': game[3]}
                            new_rows.append(new_row)
                        games_table.update_rows(new_rows)

                    publisher_names = queries.get_publisher_names()
                    ui.select(label='Select publisher', options=publisher_names, with_input=True, on_change=filter_update).bind_value_to(publisher_select_value, 'publisher')
                
                    ui.separator().classes('w-128')
                    with ui.splitter(limits=(50,50)).classes('mx-auto') as splitter:
                        with splitter.before:
                            with ui.column().classes('mr-24'):
                                ui.markdown('####Sort Type')
                                sorting_radio = ui.radio(['Title', 'Genre', 'Release Date', 'Rating'], value='Title', on_change=filter_update)
                        with splitter.after:
                            with ui.column().classes('ml-24'):
                                ui.markdown('####Order')
                                order_radio = ui.radio(['Ascending', 'Descending'], value='Ascending', on_change=filter_update)
                    ui.separator().classes('w-128')
                    games_table = ui.table(columns=columns, rows=rows, pagination=10).classes('mx-auto w-full')

@ui.page('/genres', dark=True)
def genres_page():
    header()
    with ui.column().classes('mx-auto'):
        ui.markdown('# Genres Page')
    
        # Display all genres
        def display_genres_table():
            genres = queries.get_genres()
            c = [
                # name = no clue tbh, label = what the column is called (user sees this), field = key in which we will search for the rows
                {'name': 'name', 'label': 'Name', 'field': 'name'} # col 1 : get the genre
            ]
            if genres:
                r = []
                for gen in genres:
                    r.append({'name': gen[1]})
                ui.table(columns=c, rows=r, pagination=10).classes('mx-auto')
            else:
                ui.markdown('Error! No Genres found.')
        with ui.tabs().classes('mx-auto') as tabs:
            all_genres_tab = ui.tab('All Genres')
            search_genres_tab = ui.tab('Games by Genre')
        with ui.tab_panels(tabs, value=all_genres_tab).classes('w-full mx-auto'):
            with ui.tab_panel(all_genres_tab).classes('w-full mx-auto'):
                with ui.column().classes('mx-auto w-full'):
                    display_genres_table()
            with ui.tab_panel(search_genres_tab).classes('w-full mx-auto'):
                with ui.column().classes('mx-auto w-full'):
                    columns =  [
                        # name = no clue tbh, label = what the column is called (user sees this), field = key in which we will search for the rows
                        {'name': 'title', 'label': 'Title', 'field': 'title'}, # col 1 : title from "title"
                        {'name': 'release', 'label': 'Release Date', 'field': 'release_date'}, # col 2 : release date from 'release_date'
                        {'name': 'pub', 'label': 'Publisher', 'field': 'publisher'}, # col 3 : publisher from 'pub_name'
                        {'name': 'rating', 'label': 'Rating', 'field': 'rating'} # col 4 : rating from avg <- AVG(rating) grouped by distinct games
                    ]
                    rows = []
                    games = []

                    for game in games:
                        rows.append({'title': game[0], 'release_date': game[4], 'publisher': game[2], 'rating': game[3]})
    
                    sorting_radio = None
                    order_radio = None
                    genre_select_value = {}

                    def filter_update():
                        games = queries.get_games_by_genre_name(genre_name = genre_select_value['genre'], sorting=sorting_radio.value, order=order_radio.value)
                        new_rows = []
                        for game in games:
                            new_row = {'title': game[0], 'release_date': game[4], 'publisher': game[2], 'rating': game[3]}
                            new_rows.append(new_row)
                        games_table.update_rows(new_rows)

                    genre_names = queries.get_genre_names()
                    ui.select(label='Select genre', options=genre_names, with_input=True, on_change=filter_update).bind_value_to(genre_select_value, 'genre')
                
                    ui.separator().classes('w-128')
                    with ui.splitter(limits=(50,50)).classes('mx-auto') as splitter:
                        with splitter.before:
                            with ui.column().classes('mr-24'):
                                ui.markdown('####Sort Type')
                                sorting_radio = ui.radio(['Title', 'Publisher', 'Release Date', 'Rating'], value='Title', on_change=filter_update)
                        with splitter.after:
                            with ui.column().classes('ml-24'):
                                ui.markdown('####Order')
                                order_radio = ui.radio(['Ascending', 'Descending'], value='Ascending', on_change=filter_update)
                    ui.separator().classes('w-128')
                    games_table = ui.table(columns=columns, rows=rows, pagination=10).classes('mx-auto w-full')
                
@ui.page('/users', dark=True)
def users_page():
    header()
    with ui.column().classes('mx-auto'):
        ui.markdown('# Users Page')
        ui.separator()
    
        username_text = {'data' : 'No user found'}
        # get list of usernames and store in user_names
        # this will be used for auto completion of user text box
        users_list = queries.get_all_usernames()
        user_names = []
        for user, in users_list:
            user_names.append(user)
    
        with ui.tabs().classes('mx-auto') as tabs:
            reviews_tab = ui.tab('reviews')
            games_tab = ui.tab('games')
        with ui.tab_panels(tabs, value=reviews_tab).classes('w-auto mx-auto'):
            with ui.tab_panel(reviews_tab):
                reviews_col = ui.column()
            with ui.tab_panel(games_tab):
                games_col = ui.column()
    
        def search_update():
            reviews_col.clear()
            games_col.clear()
            selected_user = search_input.value
            user_data = queries.get_user_info_by_name(selected_user)
            if user_data is None:
                username_text['data'] = 'No user found'
            else:
                username_text['data'] = f"{'Admin' if user_data[1] else 'User'}: {user_data[0]}"
                selected_user_id = queries.get_user_id(user_data[0])
                display_user_reviews(reviews_col, selected_user_id)
                display_user_games(games_col, selected_user_id)
        
        search_input = ui.input(label='Search users by username', placeholder='start typing', autocomplete=user_names, on_change=search_update).classes('w-64')
        ui.label().bind_text_from(username_text, 'data')

@ui.page('/admin', dark=True)
def admin_page():
    if not valid_admin_session():
        ui.navigate.to('/')
        return
    header()
    with ui.column().classes('mx-auto'):
        ui.markdown('# Admin Page')
        
        # FUNCTIONALITY
        # ADD PUBLISHERS, GAMES, & GENRES || REMOVE GAMES, GENRES, PUBLISHERS, USERS, & REVIEWS
        # ...
        input_values = {}
        def create_input(label, key): # INPUT LABEL CONSTRUCTOR
            def on_input_change(e):
                input_values[key] = e.value
            ui.input(label, on_change=lambda e: on_input_change(e))
            # create_input('PUBLIC LABEL', 'key') <- constructor command
            # input_values['key'] now equals whatever the user input is
    
        def add_publisher():
            create_input('publisher name', 'pub_name')
            def on_submit():
                if not input_values.get('pub_name'):
                    return
                queries.add_publisher(input_values['pub_name'])
                ui.notify('Added')
                ui.navigate.reload()
            ui.button('Add Publisher', on_click=on_submit)
        
        def remove_publisher():
            publishers = queries.get_publishers()
            pub_select = ui.select(label='select publisher', options=publishers, with_input=True)
            def on_submit():
                if not pub_select.value:
                    return
                pub_id = pub_select.value[0]
                if queries.remove_publisher(pub_id):
                    ui.notify('Removed')
                    ui.navigate.reload()
                else:
                    ui.notify('Cannot remove publisher as they have games listed')
            ui.button('Remove Publisher', on_click=on_submit)
    
        def add_genre():
            create_input('genre name', 'genre_name')
            def on_submit():
                if not input_values.get('genre_name'):
                    return
                queries.add_genre(input_values['genre_name'])
                ui.notify('Added')
                ui.navigate.reload()
            ui.button('Add Genre', on_click=on_submit)
    
        def remove_genre():
            genres = queries.get_genres()
            gen_select = ui.select(label='remove genre', options=genres, with_input=True)
            def on_submit():
                if not gen_select.value:
                    return
                genre_id = gen_select.value[0]
                if queries.remove_genre(genre_id):
                    ui.notify('Removed')
                else:
                    ui.notify('Cannot remove genre as they have games listed')
                ui.navigate.reload()
            ui.button('Remove Genre', on_click=on_submit)
            pass
    
        def add_game():
            # FIRST => get the relevant information for game (title, release_date, publisher)
            # SECOND => add the game to the DB
            # THIRD => give the game a genre => gamegenre(game_id, genre_id)
            create_input('game title', 'title')
            create_input('release date (YYYY-MM-DD)', 'release_date')
            publishers = queries.get_publishers()
            pub_select = ui.select(label='select publisher', options=publishers, with_input=True)
            genres = queries.get_genres()
            gen_select = ui.select(label='select genre', options=genres, with_input=True)
            def on_submit():
                if not pub_select.value:
                    ui.notify('No publisher selected')
                    return
                if not gen_select.value:
                    ui.notify('No genre selected')
                    return
                if not input_values.get('title') or not input_values.get('release_date'):
                    ui.notify('Title is empty or not valid')
                    return 
                if not input_values.get('release_date'):
                    ui.notify('Release date is empty or not valid')
                    return
                pub_id = pub_select.value[0]
                genre_id = gen_select.value[0]
    
                if queries.get_genre_by_id(genre_id) is None:
                    ui.notify('Genre does not exist!')
                    return
    
                if queries.add_game(input_values['release_date'], input_values['title'],pub_id, genre_id):
                    ui.notify('Adding game')
                else:
                    ui.notify('Failed to add Game Row and/or GameGenre Row')
        
                ui.navigate.reload()
            ui.button('Add Game', on_click=on_submit)
    
        def remove_game():
            games = queries.get_games()
            game_select = ui.select(label='select game', options=games, with_input=True)
            def on_submit():
                if not game_select.value:
                    return
                game_id = game_select.value[0]
    
                if queries.remove_game(game_id):
                    ui.notify('Removed')
                else:
                    ui.notify('Cannot remove game')
                ui.navigate.reload()
            ui.button('Remove Game', on_click=on_submit)
    
        def manage_user():
            # get and display users
            users_list = queries.get_all_usernames()
            user_names = []
            for user, in users_list:
                user_names.append(user)
            
            visibility = {'visible':False}
            users_section_container = ui.column()
            delete_row = ui.row().bind_visibility_from(visibility, 'visible')
            delete_row.move(users_section_container)
            tabs_container = ui.row().bind_visibility_from(visibility, 'visible')
            with users_section_container:
                with tabs_container:
                    with ui.tabs() as tabs:
                        reviews_tab = ui.tab('reviews')
                        games_tab = ui.tab('games')
                    with ui.tab_panels(tabs, value=reviews_tab):
                        with ui.tab_panel(reviews_tab):
                            reviews_col = ui.column()
                        with ui.tab_panel(games_tab):
                            games_col = ui.column()
    
            # with chosen user, display their profile
            def see_profile():
                visibility['visible'] = False
                if search_input.value not in user_names:
                    return
                reviews_col.clear()
                games_col.clear()
                delete_row.clear()
                user_name = search_input.value
                selected_user_id = queries.get_user_id(user_name)
                display_user_reviews(reviews_col, selected_user_id)
                display_user_games(games_col, selected_user_id)
                visibility['visible'] = True
                # press to delete user
                def on_delete():
                    user_id = app.storage.user['session']
                    if (user_id == selected_user_id[0]):
                        ui.notify('Cannot remove yourself!')
                        return
                    queries.remove_user(selected_user_id)
                    ui.notify('Removed user!')
                    ui.navigate.reload()
                def on_toggle_admin():
                    user_id = app.storage.user['session']
                    if (user_id == selected_user_id[0]):
                        ui.notify('Cannot change your own admin status!')
                        return
                    queries.toggle_admin(selected_user_id)
                    admin_status = queries.is_admin(selected_user_id)
                    ui.notify(f'Set admin status to {admin_status}')
                with delete_row:
                    ui.button('Remove User', on_click=on_delete)
                    ui.button('Toggle Admin Status', on_click=on_toggle_admin)
                    
            with users_section_container:
                search_input = ui.select(label='Search users by username', options=user_names, on_change=see_profile).classes('w-64')
                search_input.move(target_index=0)

        def remove_review():
            # get and display users
            users_list = queries.get_all_usernames()
            user_names = []
            for user, in users_list:
                user_names.append(user)
    
            dropdown_container = ui.row()
    
            # with chosen user, display their reviews
            def see_reviews():
                dropdown_container.clear()
                if search_input.value not in user_names:
                    return
                u = search_input.value
                user_id = queries.get_user_id(u)
                reviews_of_user = queries.get_reviews_by_user_adminview(user_id) #seven-eleven
                if reviews_of_user is None:
                    with dropdown_container:
                        ui.label('User has no reviews')
                    return
                with dropdown_container:
                    rev_select = ui.select(options=reviews_of_user, with_input=True)
                # press to delete review
                def on_submit():
                    if not rev_select.value:
                        ui.notify('No Review Selected')
                        return
                    review_id = rev_select.value[0]
                    if queries.remove_review(review_id):
                        ui.notify('Removed')
                        ui.navigate.reload()
                with dropdown_container:
                    ui.button('Remove Review', on_click=on_submit)
    
            search_input = ui.select(label='Search users by username', options=user_names, on_change=see_reviews).classes('w-64')
    
    
    
        # TABS : contains one for each appropriate category (pub, genre, game, ...)
        # Each tab may contain ADD or REMOVE function (some may not have an ADD function, but all will have a REMOVE function)
        with ui.tabs().classes('mx-auto') as tabs:
            pub_tab = ui.tab('Manage Publishers')
            genre_tab = ui.tab('Manage Genres')
            game_tab = ui.tab('Manage Games')
            user_tab = ui.tab('Manage Users')
            review_tab = ui.tab('Manage Reviews')
        with ui.tab_panels(tabs,value=pub_tab).classes('w-auto mx-auto'):
            with ui.tab_panel(pub_tab):
                ui.label('ADD PUBLISHER')
                add_publisher()
                ui.label()
                ui.separator()
                ui.label()
                ui.label('REMOVE PUBLISHER')
                remove_publisher()
            with ui.tab_panel(genre_tab):
                ui.label('ADD GENRE')
                add_genre()
                ui.label()
                ui.separator()
                ui.label()
                ui.label('REMOVE GENRE')
                remove_genre()
                pass
            with ui.tab_panel(game_tab):
                ui.label('ADD GAME')
                add_game()
                ui.label()
                ui.separator()
                ui.label()
                ui.label('REMOVE GAME')
                remove_game()
                pass
            with ui.tab_panel(user_tab):
                ui.label('MANAGE USER')
                manage_user()
                ui.label()
                pass
            with ui.tab_panel(review_tab):
                ui.label('REMOVE REVIEW')
                remove_review()
                pass

# REMOVE THIS PAGE ? - OBSOLETE 
@ui.page('/reviews', dark=True)
def reviews_page():
    header()
    with ui.column().classes('mx-auto'):
        ui.markdown('# Reviews Page')
        ui.separator()
        reviews = queries.get_all_reviews()
        for review in reviews:
            ui.label(f"Rating: {review[1]} | Title: {review[3]} | Description: {review[2]}")
            ui.separator()
        
        #review search box -> select a game (with autocompletion) -> display all reviews for said game
        #options = queries.get_games()
        #ui.input(label='Text', placeholder='start typing', autocomplete=options).props('clearable')

@ui.page('/profile', dark=True)
def profile_page():
    header()
    if not valid_session():
        ui.navigate.to('/')
        return
    user_id = app.storage.user.get('session')
    # check if user is logged in
    if not user_id:
        ui.navigate.to('/register')
    
    input_values = {'description':'', 'title':0}
    def create_input(label, key, max_length):
        def on_input_change(e):
            input_values[key] = e.value
        new_input = ui.input(label, on_change=lambda e: on_input_change(e), validation={f'Input too long (limit {max_length} characters)': lambda value: len(value) <= max_length})
        new_input.classes('w-full')
    def create_text_area(label, key, max_length):
        def on_input_change(e):
            input_values[key] = e.value
        new_textarea = ui.textarea(label, on_change=on_input_change, validation={f'Input too long (limit {max_length} characters)': lambda value: len(value) <= max_length})
        new_textarea.classes('w-full')
    with ui.column().classes('mx-auto'):
        with ui.tabs().classes('mx-auto') as tabs:
            reviews_tab = ui.tab('My Reviews')
            games_tab = ui.tab('Played Games')
            add_game_tab = ui.tab('Manage Games')
            add_review_tab = ui.tab('Add Reviews')
            remove_review_tab = ui.tab('Remove Reviews')
            manage_account_tab = ui.tab('Manage Account')
        with ui.tab_panels(tabs, value=reviews_tab).classes('w-full mx-auto'):
            with ui.tab_panel(reviews_tab):
                reviews_col = ui.column().classes('mx-auto w-full')
            with ui.tab_panel(games_tab):
                games_col = ui.column().classes('mx-auto w-full')
            with ui.tab_panel(add_game_tab):
                games = queries.get_game_titles()
                with ui.column().classes('mx-auto w-full'):
                    if (games):
                        game_select_value = {}
                        game_select = ui.select(label='Select game', options=games, with_input=True).bind_value_to(game_select_value, 'game')
                        def on_add():
                            if not game_select_value.get('game'):
                                ui.notify('Please select a game')
                                return
                            if game_select_value['game'] not in queries.get_unplayed_games_by_user_id(user_id):
                                ui.notify('Game already added!')
                                return
                            game_id = queries.get_game_id(game_select_value['game'])
                            queries.add_user_game(user_id, game_id)
                            ui.navigate.reload()
                        def on_remove():
                            if not game_select_value.get('game'):
                                ui.notify('Please select a game')
                                return
                            if game_select_value['game'] in queries.get_unplayed_games_by_user_id(user_id):
                                ui.notify('Game not played!')
                                return
                            game_id = queries.get_game_id(game_select_value['game'])
                            queries.remove_user_game(user_id, game_id)
                            ui.navigate.reload()
                        with ui.button_group():
                            ui.button('Add Game', on_click=on_add)
                            ui.button('Remove Game', on_click=on_remove)
                    else:
                        ui.label('No Games')

            with ui.tab_panel(add_review_tab):
                # check if the user has "played" games
                games = queries.get_game_titles_by_user_id(user_id)
                with ui.column().classes('mx-auto w-full'):
                    if (games):
                        game_select = ui.select(label='Select game', options=games, with_input=True)
                        with ui.row().classes('w-full'):
                            ui.label('Rating:')
                            ui.slider(min=0, max=5, value=0).bind_value_to(input_values, 'rating').classes('w-6/12')
                            ui.label().bind_text_from(input_values, 'rating')
                        create_input('Title', 'title', 100)
                        create_text_area('Description', 'description', 500)
                        def on_submit():
                            if not game_select.value:
                                ui.notify('Please select a game')
                                return
                            if input_values['title'] == 0:
                                ui.notify('Please write a title')
                                return
                            game_id = queries.get_game_id(game_select.value)
                            if game_id in queries.get_game_id_reviews_by_user(user_id):
                                ui.notify('Already wrote a review for this game!')
                                return
                            queries.add_review(user_id, game_id, input_values['title'], input_values['description'], input_values['rating'])
                            ui.navigate.reload()
                        ui.button('Submit Review', on_click=on_submit)                            
                    else:
                        ui.label('There are no games in your library to review')
            
            with ui.tab_panel(remove_review_tab):
                reviews = queries.get_reviews_by_user_id_public(user_id)
                with ui.column().classes('mx-auto w-full'):
                    if (reviews):
                        reviews_select = ui.select(label='Select review', options=reviews, with_input=True)
                        def on_submit():
                            if not reviews_select.value:
                                ui.notify('Please select a review')
                                return
                            game_id = queries.get_game_id(reviews_select.value[0])
                            review_id = queries.get_review_id_by_user_game_id(user_id, game_id)
                            queries.remove_review(review_id)
                            ui.notify('Removed Review')
                            ui.navigate.reload()
                        ui.button('Remove Review', on_click=on_submit)
                    else:
                        ui.label('You have no reviews')
            with ui.tab_panel(manage_account_tab):
                with ui.column().classes('mx-auto w-full'):
                    manage_account_values = {}
                    def create_input_password(label, key):
                        def on_input_change(e):
                            manage_account_values[key] = e.value
                        ui.input(label, password=True, on_change=lambda e: on_input_change(e)).classes('mx-auto w-1/2')
                    create_input_password('Type new password', 'new_password')
                    create_input_password('Type in current password', 'old_password')
                    def change_password():
                        if manage_account_values.get('old_password') and manage_account_values.get('new_password'):
                            if len(manage_account_values['new_password']) < 12:
                                ui.notify('Password length too short! Minimum 12 characters')
                                return
                            user_name = queries.get_user_name(user_id)
                            if queries.authenticate_login(user_name, manage_account_values['old_password']):
                                if manage_account_values['old_password'] == manage_account_values['new_password']:
                                    ui.notify('New password is already being used!')
                                    return
                                hashed_password = bcrypt.hashpw(manage_account_values['new_password'].encode('utf-8'), bcrypt.gensalt())
                                queries.change_password(user_id, hashed_password.decode('utf-8'))
                                logout_button()
                            else:
                                ui.notify('Incorrect password')
                        else:
                            ui.notify('Missing one or more required fields')
                    
                    def remove_account():
                        if manage_account_values.get('old_password'):
                            user_name = queries.get_user_name(user_id)
                            if queries.authenticate_login(user_name, manage_account_values['old_password']):
                                queries.remove_user(user_id)
                                del app.storage.user['session']
                                ui.navigate.to('/')
                            else:
                                ui.notify('Incorrect password')
                        else:
                            ui.notify('Type in current password to delete your account')

                    with ui.button_group().classes('mx-auto'):
                        ui.button('Change password', on_click=change_password)
                        ui.button('Delete account', on_click=remove_account)
    display_user_reviews(reviews_col, user_id)
    display_user_games(games_col, user_id)

@ui.page('/login', dark=True)
def login_page():
    if valid_session():
        ui.navigate.to('/')
        return
    with ui.column().classes('mx-auto'):
        ui.markdown('# Login Page')
        ui.separator()
        input_values = {}
    
        def create_input(label, key):
            def on_input_change(e):
                input_values[key] = e.value
            ui.input(label, on_change=lambda e: on_input_change(e))
    
        def create_input_password(label, key):
            def on_input_change(e):
                input_values[key] = e.value
            ui.input(label, password=True, on_change=lambda e: on_input_change(e))
    
        create_input('Username', 'username')
        create_input_password('Password', 'password')
    
        def login_button():
            if (input_values['username'] and input_values['password']):
                # username and password fields provided
                if queries.authenticate_login(input_values['username'], input_values['password']):
                    app.storage.user['session'] = queries.get_user_id(input_values['username'])[0]
                    ui.notify('LOGIN SUCCESSFUL')
                    ui.navigate.to('/')
                else:
                    ui.notify('INCORRECT USERNAME OR PASSWORD')
            else:
                ui.notify('USERNAME OR PASSWORD FIELDS MISSING')
    
        ui.button('Login', on_click=login_button)
        ui.link('Don\'t have an account?', register_page).classes('text-white text-2x1')

@ui.page('/register', dark=True)
def register_page():
    if valid_session():
        ui.navigate.to('/')
        return
    with ui.column().classes('mx-auto'):
        ui.markdown('# Register Page')
        ui.separator()
        input_values = {}
    
        def create_input(label, key):
            def on_input_change(e):
                input_values[key] = e.value
            ui.input(label, on_change=lambda e: on_input_change(e))
    
        def create_input_password(label, key):
            def on_input_change(e):
                input_values[key] = e.value
            ui.input(label, password=True, on_change=lambda e: on_input_change(e))
    
        create_input('Username', 'username')
        create_input('Email', 'email')
        create_input_password('Password', 'password')
        create_input_password('Retype Password', 'password2')
        
        admin = False
        def register_button():
            if (input_values['username'] and input_values['email'] and input_values['password'] 
                and input_values['password2'] and (input_values['password'] == input_values['password2'])):
                hashed_password = bcrypt.hashpw(input_values['password2'].encode('utf-8'), bcrypt.gensalt())
                if len(input_values['password']) < 12:
                    ui.notify('Password length too short! Minimum 12 characters')
                    return
                if queries.add_user(input_values['username'], input_values['email'], hashed_password.decode('utf-8'), admin):
                    ui.notify('USER ADDED!', type='positive')
                    ui.navigate.to('/login')
                else:
                    ui.notify('USERNAME OR EMAIL ALREADY TAKEN', type='warning')
            else:
                ui.notify('MISSING OR INCORRECT FIELD', type='negative')
    
        ui.button('Register', on_click=register_button)

def header():
    

    with ui.header():
        ui.link('HOME', home_page).classes('text-white no-underline hover:underline text-2xl')
        ui.link('GAMES', games_page).classes('text-white no-underline hover:underline text-2xl')
        ui.link('USERS', users_page).classes('text-white no-underline hover:underline text-2xl')
        ui.link('PUBLISHERS', publishers_page).classes('text-white no-underline hover:underline text-2xl')
        #ui.link('REVIEWS', reviews_page).classes('text-white no-underline hover:underline text-2xl')
        ui.link('GENRES', genres_page).classes('text-white no-underline hover:underline text-2xl')
        
        
        if valid_session():
            ui.space()
            ui.link('PROFILE', profile_page).classes('text-white no-underline hover:underline text-2xl')
            ui.button('LOGOUT', on_click=logout_button).classes('text-white no-underline hover:underline text-2x1')
        else:
            ui.space()
            ui.link('LOGIN', login_page).classes('text-white no-underline hover:underline text-2xl')
            ui.link('REGISTER', register_page).classes('text-white no-underline hover:underline text-2xl')

        if valid_admin_session():
            ui.link('ADMIN', admin_page).classes('text-white no-underline hover:underline text-2xl')

def valid_session():
    user_id = app.storage.user.get('session')
    # if cookie is stored but its not valid, delete it and return False
    if user_id and not queries.user_id_exists(user_id):
        del app.storage.user['session']
        return False
    # if cookie is stored and its valid, return True
    if user_id and queries.user_id_exists(user_id):
        return True
    # all else return False
    return False

def valid_admin_session():
    user_id = app.storage.user.get('session')
    if not user_id:
        return False
    if valid_session() and queries.is_admin(user_id):
        return True
    return False

def display_user_reviews(container, user_id):
    username = queries.get_user_name(user_id)
    reviews = queries.get_reviews_by_user_name(username)
    with container:
        ui.markdown(f"# {username[0]}'s reviews")
        ui.separator()
        if reviews is None:
            ui.label("No reviews found")
        else:
            for review in reviews:
                with ui.column():
                    ui.markdown(f"### {review[3]}")
                    with ui.row():
                        [ui.icon('star') for _ in range(int(review[2]))]
                    ui.markdown(f"#### {review[0]}")
                    ui.markdown(f"###### {review[1]}")
                ui.separator()

def display_user_games(container, user_id):
    username = queries.get_user_name(user_id)
    games = queries.get_games_by_user_id(user_id)
    with container:
        ui.markdown(f"# {username[0]}'s games")
        ui.separator()
        if games is None:
            ui.label("No games found")
        else:
            for game in games:
                with ui.column():
                    ui.markdown(f"### {game[0]}")
                    ui.markdown(f"###### Released: {game[3]}")
                    ui.markdown(f"###### Publisher: {game[2]}")
                    ui.markdown(f"###### Genre: {game[1]}")
                ui.separator()

def logout_button():
    if valid_session():
        del app.storage.user['session']
        ui.navigate.to('/')
        ui.navigate.reload()

ui.run(title='Project Website', storage_secret='private key to secure the browser session cookie')