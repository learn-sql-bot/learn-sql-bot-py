async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Привет! Начнем что нибудь решать?")
