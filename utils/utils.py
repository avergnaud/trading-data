import base64
import io


def pyplotToBase64Img(plt):
    my_string_i_obytes = io.BytesIO()
    plt.savefig(my_string_i_obytes, format='png')
    my_string_i_obytes.seek(0)
    return base64.b64encode(my_string_i_obytes.read())
