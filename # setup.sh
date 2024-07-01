mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[global]\n\
legacyTheme = false\n\
\n\
" > ~/.streamlit/config.toml
