from plumbum import cli
from hacking_hogwarts.sorting_hat import SortingHat 
from hacking_hogwarts.time_quiz.time_quiz_sorting_hat import TimeQuizSortingHat

def generate_sorting_hat_model(sorting_hat_type):
    sorting_hat_model = None
    if sorting_hat_type == "time_quiz":
        sorting_hat_model = TimeQuizSortingHat
    return sorting_hat_model

class SortingHatApp(cli.Application):
    pass

class SortingHatTrainApp(cli.Application):
    sorting_hat_type =  cli.SwitchAttr(
        ['--type'],
        argtype=cli.Set('time_quiz'), 
        default='time_quiz',
        help='Which type of sorting hat model',
    )
    dataframe = cli.SwitchAttr(
        ['--dataframe'],
        argtype=str,
        mandatory=True,
        help='Path to pkl dataframe',
    )

    output = cli.SwitchAttr(
        ['--output'],
        argtype=str,
        mandatory=True,
        help='Path to pkl output',
    )

    def main(self):
        sorting_hat_model = generate_sorting_hat_model(self.sorting_hat_type)
        sorting_hat = sorting_hat_model()
        sorting_hat.load_dataframe(dataframe_path=self.dataframe)
        sorting_hat.train()
        sorting_hat.evaluate()
        sorting_hat.save(self.output)

class SortingHatPredictApp(cli.Application):
    sorting_hat_type =  cli.SwitchAttr(
        ['--type'],
        argtype=cli.Set('time_quiz'), 
        default='time_quiz',
        help='Which type of sorting hat model',
    )
    model = cli.SwitchAttr(
        ['--model'],
        argtype=str,
        mandatory=True,
        help='Path to hdf5 model',
    )

    json_input = cli.SwitchAttr(
        ['--json_input'],
        argtype=str,
        mandatory=True,
        help='JSON of input',
    )

    def main(self):
        import json

        sorting_hat_model = generate_sorting_hat_model(self.sorting_hat_type)
        sorting_hat = sorting_hat_model()
        sorting_hat.load_model(model_path=self.model)
        prediction = sorting_hat.predict(inputs=json.loads(self.json_input))
        print(prediction)


SortingHatApp.subcommand("train", SortingHatTrainApp)
SortingHatApp.subcommand("predict", SortingHatPredictApp)

if __name__ == '__main__':
    SortingHatApp.run()
