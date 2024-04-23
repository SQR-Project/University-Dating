import streamlit as st

def main():
    # Массив с путями к картинкам
    images = [
        "/Users/k.tyulebaeva/inno/University-Dating/app/src/ui/pics/meme.jpg",
        "/Users/k.tyulebaeva/inno/University-Dating/app/src/ui/pics/meme2.jpg",
        "/Users/k.tyulebaeva/inno/University-Dating/app/src/ui/pics/meme3.jpg"
    ]

    current_image_index = 0  # Индекс текущей отображаемой картинки

    while True:
        st.title("Галерея изображений")
        st.image(images[current_image_index], use_column_width=True)
        
        # Вывод кнопок для листания изображений
        if current_image_index > 0:
            st.button("Предыдущая", key='prev_button')
        if current_image_index < len(images) - 1:
            st.button("Следующая", key='next_button')

        # Обработка событий кнопок
        event = st.experimental_get_query_params().get("button_clicked")
        if event:
            if event[0] == "prev_button":
                current_image_index -= 1
            elif event[0] == "next_button":
                current_image_index += 1

        # Блокировка обновления страницы при изменении состояния
        st.experimental_set_query_params(button_clicked=None)
        st.stop()

if __name__ == "__main__":
    main()