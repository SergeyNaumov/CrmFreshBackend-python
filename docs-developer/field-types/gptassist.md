# `GPTAssist` — плагин, не тип поля

`GPTAssist` — это **плагин** к полю [`text`](text.md) / [`wysiwyg`](wysiwyg.md),
а не отдельный `type`. Подключается через `plugins`.

## Атрибуты плагина

| Ключ | Смысл |
|---|---|
| `type` | `'GPTAssist'` |
| `set_value_button` | текст кнопки, которая подставит ответ GPT в поле |

## Пример

```python
{
  'description': 'Описание',
  'type': 'wysiwyg',
  'name': 'body',
  'filedir': './files/project_5830/good',
  'plugins': [
     {'type': 'GPTAssist', 'set_value_button': 'Отправить в описание'},
  ],
}
```

## Особенности

- Компонент: `src/components/GPTAssist/GPTAssist`.
- Кнопка подставляет сгенерированный текст в значение поля.
- Настройки GPT задаются на уровне проекта (не в каждом конфиге).
