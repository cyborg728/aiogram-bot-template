 with I18nContext.with_current(
            self.new_context(
                locale=cast(str, locale or self.core.default_locale),
                data=data,
            )
        ) as context:
            data[self.context_key] = context
            yield context

# LOCALE INSIDE CONTEXT 