import random

import cryptography
from cryptography.fernet import Fernet


def generate_random_file():
    with open("random.txt", "wb") as f:
        for _ in range(1024 * 1024):
            f.write(random.randbytes(8))


def encrypt(filename: str, key: str):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename: str, key: bytes):
    f = Fernet(key)

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        return

    with open(filename, "wb") as file:
        file.write(decrypted_data)

    # def time_based_chunks(self):
    #     self.chunk_counter = 0
    #     with open(self.file_name, "rb") as f:
    #         while True:
    #             start_time = (
    #                 datetime.now()
    #             )  # time the transfer of the previous chunk started
    #             content = f.read(self.chunk_size_estimate)
    #             if not content:
    #                 break
    #             yield content
    #             self.chunk_counter += 1
    #             end_time = (
    #                 datetime.now()
    #             )  # time the transfer of the current chunk ended
    #             transfer_time = end_time - start_time
    #             if self.chunk_counter % self.window_size == 0:
    #                 # use a sliding window to estimate the rate of data transfer
    #                 past_transfers = [transfer_time] * self.window_size
    #                 transfer_rate = sum(past_transfers, timedelta(0)) / self.window_size
    #                 # predict the time required to transfer the remaining data
    #                 remaining_bytes = os.stat(self.file_name).st_size - f.tell()
    #                 remaining_time_estimate = (
    #                     remaining_bytes / transfer_rate.total_seconds()
    #                 )
    #                 # adjust the chunk size based on the predicted time to optimize transfer time
    #                 self.chunk_time_estimate = (
    #                     remaining_time_estimate / self.window_size
    #                 )
    #                 self.chunk_size_estimate = int(
    #                     max(
    #                         min(
    #                             self.chunk_size_estimate,
    #                             remaining_bytes / (self.chunk_time_estimate + 1),
    #                         ),
    #                         1,
    #                     )
    #                 )

    # def secure_chunks(self):
    #     with open(self.file_name, "rb") as f:
    #         while content := f.read(self.chunk_size_estimate):
    #             yield content
    #             self.chunk_counter += 1
    #             if self.chunk_counter % self.window_size == 0:
    #                 # use a sliding window to estimate the collision probability
    #                 past_hashes = self.hasher.digest() * self.window_size
    #                 self.hasher = hashlib.sha256()
    #                 self.hasher.update(past_hashes)
    #                 collision_probability = 1 - (1 - 1 / 2**256) ** self.window_size
    #                 # adjust the chunk size based on the collision probability
    #                 self.chunk_size_estimate = int(
    #                     max(
    #                         min(
    #                             self.chunk_size_estimate,
    #                             math.sqrt(
    #                                 0.5
    #                                 / collision_probability
    #                                 * os.stat(self.file_name).st_size
    #                             ),
    #                         ),
    #                         1,
    #                     )
    #                 )


if __name__ == "__main__":
    generate_random_file()
    # key = base64.urlsafe_b64encode(hashlib.sha256(b"password").digest())

    # decrypt("random.txt", key)
    # encrypt("random.txt", key)
