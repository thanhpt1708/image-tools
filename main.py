from PIL import Image
import os


def resize_and_compress_images(
    input_folder, output_folder, target_width, max_file_size
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(
            (".png", ".PNG", ".jpg", ".JPG", ".JPEG", ".jpeg", ".WEBP", ".webp")
        ):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            with Image.open(input_path) as img:
                output_quality = 85

                # Calculate height while keeping aspect ratio
                ratio = target_width / float(img.size[0])
                target_height = int(float(img.size[1]) * ratio)

                # Resize the image
                img.thumbnail((target_width, target_height))

                # Adjust height if width is not exactly target_width
                if img.size[0] != target_width:
                    img = img.resize((target_width, target_height))

                # Compress the image to reduce file size
                img.save(output_path, optimize=True, quality=output_quality)

                # Check and adjust file size
                while os.path.getsize(output_path) > max_file_size:
                    # If file size exceeds the limit, further compress the image
                    output_quality -= 1
                    img.save(output_path, optimize=True, quality=output_quality)
                print(f"Processed: {output_path}")


if __name__ == "__main__":
    # Example usage
    input_folder = os.getcwd()
    output_folder = "output_images"
    target_width = 1600
    max_file_size = 200 * 1024  # 200KB

    resize_and_compress_images(input_folder, output_folder, target_width, max_file_size)
